from sqlalchemy import Column, String, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from app.models.base_model import BaseDBModel

class Document(BaseDBModel):
    """文档模型，支持无限层级结构"""
    __tablename__ = "documents"

    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="文档ID"
    )
    
    title: str = Column(
        String(200), 
        nullable=False,
        index=True,
        comment="文档标题"
    )
    content: str = Column(
        Text,
        nullable=True,
        default="",
        comment="文档内容"
    )
    parent_id: int = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="父文档ID"
    )
    path: str = Column(
        String(1000),
        nullable=False,
        comment="文档路径，格式：/1/2/3/"
    )
    level: int = Column(
        Integer,
        nullable=False,
        default=1,
        comment="文档层级，从1开始"
    )
    sort_order: int = Column(
        Integer,
        nullable=False,
        default=1,
        comment="同级排序"
    )
    doc_type: str = Column(
        String(20),
        nullable=False,
        default="markdown",
        comment="文档类型：markdown, rich_text, knowledge"
    )
    creator_id: int = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="创建者ID"
    )
    editor_id: int = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="最后编辑者ID"
    )
    
    # 关系
    parent = relationship(
        "Document",
        remote_side=[id],
        backref="children",
        lazy="joined"
    )
    creator = relationship(
        "User",
        foreign_keys=[creator_id],
        lazy="select"
    )
    editor = relationship(
        "User",
        foreign_keys=[editor_id],
        lazy="select"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.creator_name = None  # 创建者名称
        self.editor_name = None   # 编辑者名称
        self.path_names = None    # 路径名称

    def __repr__(self) -> str:
        return f"<Document {self.title}>" 