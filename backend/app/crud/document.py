from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentTree
from app.models.user import User

class CRUDDocument(CRUDBase[Document, DocumentCreate, DocumentUpdate]):
    def get_children(
        self,
        db: Session,
        *,
        parent_id: Optional[int] = None
    ) -> List[Document]:
        """获取子文档"""
        return db.query(Document).filter(
            and_(
                Document.parent_id == parent_id,
                Document.deleted_at.is_(None)
            )
        ).order_by(Document.sort_order.asc()).all()

    def get_document_with_path(
        self,
        db: Session,
        *,
        document_id: int
    ) -> Optional[Document]:
        """
        获取文档详细信息，包括路径和用户信息
        
        Args:
            db: 数据库会话
            document_id: 文档ID
            
        Returns:
            包含完整信息的文档对象，如果不存在则返回None
        """
        # 获取文档基本信息
        document = db.query(Document).filter(
            and_(
                Document.id == document_id,
                Document.deleted_at.is_(None)
            )
        ).first()
        
        if not document:
            return None
            
        # 获取创建者和编辑者信息
        if document.creator_id:
            creator = db.query(User).filter(User.id == document.creator_id).first()
            if creator:
                document.creator_name = creator.nickname or creator.username
                
        if document.editor_id:
            editor = db.query(User).filter(User.id == document.editor_id).first()
            if editor:
                document.editor_name = editor.nickname or editor.username
                
        # 解析路径获取所有父文档标题
        path_ids = [int(id_) for id_ in document.path.strip('/').split('/') if id_]
        if path_ids:
            parent_docs = db.query(Document.id, Document.title).filter(
                Document.id.in_(path_ids)
            ).all()
            path_titles = {doc.id: doc.title for doc in parent_docs}
            document.path_names = '/'.join(
                path_titles.get(id_, '') for id_ in path_ids
            )
        else:
            document.path_names = ''
            
        return document

    def get_tree(
        self,
        db: Session,
        *,
        parent_id: Optional[int] = None,
        max_depth: Optional[int] = None
    ) -> List[DocumentTree]:
        """
        获取文档树
        Args:
            parent_id: 父文档ID，None表示获取根文档
            max_depth: 最大深度，None表示不限制深度
        """
        # 如果指定了最大深度且小于等于0，则返回空列表
        if max_depth is not None and max_depth <= 0:
            return []
        
        # 获取当前层级的文档
        docs = self.get_children(db, parent_id=parent_id)
        
        # 构建树结构
        tree = []
        for doc in docs:
            # 递归获取子文档
            # 如果max_depth为None，继续递归；否则减少深度
            next_depth = None if max_depth is None else max_depth - 1
            children = self.get_tree(
                db,
                parent_id=doc.id,
                max_depth=next_depth
            ) if max_depth is None or max_depth > 1 else []
            
            # 构建树节点
            node = DocumentTree(
                id=doc.id,
                title=doc.title,
                doc_type=doc.doc_type,
                level=doc.level,
                sort_order=doc.sort_order,
                has_children=bool(children),
                children=children
            )
            tree.append(node)
        
        return tree

    def create_with_path(
        self,
        db: Session,
        *,
        obj_in: DocumentCreate,
        creator_id: int
    ) -> Document:
        """
        创建文档（自动处理路径）
        """
        # 获取父文档
        parent = None
        if obj_in.parent_id:
            parent = self.get(db, id=obj_in.parent_id)
            if not parent:
                raise ValueError("父文档不存在")
        
        # 计算层级和路径
        level = 1
        path = "/"
        if parent:
            level = parent.level + 1
            path = f"{parent.path}{parent.id}/"
        
        # 创建文档
        db_obj = Document(
            title=obj_in.title,
            content=obj_in.content,
            parent_id=obj_in.parent_id,
            path=path,
            level=level,
            sort_order=obj_in.sort_order or 1,
            doc_type=obj_in.doc_type,
            creator_id=creator_id,
            editor_id=creator_id
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_editor(
        self,
        db: Session,
        *,
        db_obj: Document,
        obj_in: DocumentUpdate,
        editor_id: int
    ) -> Document:
        """
        更新文档（记录编辑者）
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        update_data["editor_id"] = editor_id
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def search_documents(
        self,
        db: Session,
        *,
        keyword: Optional[str] = None,
        doc_type: Optional[str] = None,
        creator_id: Optional[int] = None,
        parent_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Document]:
        """
        搜索文档
        Args:
            keyword: 搜索关键词（标题和内容）
            doc_type: 文档类型
            creator_id: 创建者ID
            parent_id: 父文档ID
            skip: 跳过记录数
            limit: 返回记录数
        """
        query = db.query(Document).filter(Document.deleted_at.is_(None))
        
        # 关键词搜索
        if keyword:
            query = query.filter(
                or_(
                    Document.title.ilike(f"%{keyword}%"),
                    Document.content.ilike(f"%{keyword}%")
                )
            )
        
        # 文档类型过滤
        if doc_type:
            query = query.filter(Document.doc_type == doc_type)
        
        # 创建者过滤
        if creator_id:
            query = query.filter(Document.creator_id == creator_id)
        
        # 父文档过滤
        if parent_id is not None:  # 包括parent_id=0的情况
            query = query.filter(Document.parent_id == parent_id)
        
        # 排序并分页
        return query.order_by(
            Document.updated_at.desc()
        ).offset(skip).limit(limit).all()

crud_document = CRUDDocument(Document) 