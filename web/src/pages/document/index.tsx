import React, { useState, useEffect, useCallback } from 'react';
import { Card, Tree, Button, Modal, message, Typography, Menu, Input, Select } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, FolderOutlined, FileOutlined, EyeOutlined } from '@ant-design/icons';
import { documentApi } from '@/services/api/document';
import { Editor, Toolbar } from '@wangeditor/editor-for-react';
import { IDomEditor, IEditorConfig, IToolbarConfig } from '@wangeditor/editor';
import '@wangeditor/editor/dist/css/style.css';
import styles from './index.less';
import { debounce } from 'lodash';
import { history } from '@umijs/max';
import './components/CustomButton';
import { CUSTOM_BUTTON_KEY } from './components/CustomButton';

const { DirectoryTree } = Tree;
const { Title } = Typography;
const { confirm } = Modal;
const { Option } = Select;

interface TempNode extends API.DocumentTreeNode {
  isTemp?: boolean;
  parent_id?: number;
}

interface ContextMenuState {
  visible: boolean;
  x: number;
  y: number;
  node: TempNode | null;
}
const DocumentPage: React.FC = () => {
  const [treeData, setTreeData] = useState<TempNode[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<API.Document>();
  const [editingKey, setEditingKey] = useState<number | string | null>(null);
  const [editingTitle, setEditingTitle] = useState('');
  const [editor, setEditor] = useState<IDomEditor | null>(null);
  const [html, setHtml] = useState('');
  const [contextMenu, setContextMenu] = useState<ContextMenuState>({
    visible: false,
    x: 0,
    y: 0,
    node: null,
  });

  // 使用防抖的 setEditingTitle
  const debouncedSetEditingTitle = useCallback(
    debounce((value: string) => {
      setEditingTitle(value);
    }, 100),
    []
  );

  // 工具栏配置
  const toolbarConfig: Partial<IToolbarConfig> = {
    toolbarKeys: [
      'headerSelect',
      'bold',
      'italic',
      'underline',
      'through',
      'color',
      'bgColor',
      'lineHeight',
      '|',
      'bulletedList',
      'numberedList',
      'todo',
      '|',
      'insertLink',
      'insertTable',
      'codeBlock',
      'emotion',
      '|',
      'undo',
      'redo',
      'blockquote',
      '|',
      CUSTOM_BUTTON_KEY
    ],
  };

  // 编辑器配置
  const editorConfig: Partial<IEditorConfig> = {
    placeholder: '请输入内容...',
    autoFocus: false,
  };

  // 加载文档树
  const loadDocumentTree = async () => {
    try {
      const data = await documentApi.getDocumentTree();
      setTreeData(data || []);
    } catch (error: any) {
      message.error(error.message || '加载文档树失败');
    }
  };

  // 加载文档详情
  const loadDocument = async (id: number) => {
    try {
      const data = await documentApi.getDocument(id);
      setSelectedDoc(data);
    } catch (error: any) {
      message.error(error.message || '加载文档失败');
    }
  };

  useEffect(() => {
    loadDocumentTree();
  }, []);

  // 处理点击外部关闭菜单
  useEffect(() => {
    const handleClickOutside = () => {
      if (contextMenu.visible) {
        setContextMenu(prev => ({ ...prev, visible: false }));
      }
    };

    if (contextMenu.visible) {
      document.addEventListener('click', handleClickOutside);
    }

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [contextMenu.visible]);

  // 处理树节点选择
  const handleSelect = (selectedKeys: React.Key[]) => {
    const nodeId = selectedKeys[0] as number;
    if (nodeId && !isNaN(Number(nodeId)) && nodeId !== editingKey) {
      loadDocument(nodeId);
    }
  };

  // 处理标题编辑
  const handleTitleChange = async (newTitle: string) => {
    if (!selectedDoc) return;
    try {
      await documentApi.updateDocument(selectedDoc.id, {
        title: newTitle,
      });
      message.success('标题修改成功');
      loadDocument(selectedDoc.id);
      loadDocumentTree();
    } catch (error: any) {
      message.error(error.message || '标题修改失败');
    }
  };

  // 加载文档时设置编辑器内容
  useEffect(() => {
    if (selectedDoc) {
      setHtml(selectedDoc.content || '');
    }
  }, [selectedDoc]);

  // 监听编辑器内容变自动保存
  const handleEditorChange = useCallback((editor: IDomEditor) => {
    const newHtml = editor.getHtml();
    setHtml(newHtml);
    
    // 自动保存
    if (selectedDoc) {
      const timer = setTimeout(async () => {
        try {
          await documentApi.updateDocument(selectedDoc.id, {
            content: newHtml,
          });
        } catch (error: any) {
          message.error(error.message || '保存失败');
        }
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [selectedDoc]);

  // 组件销毁时销毁编辑器
  useEffect(() => {
    return () => {
      if (editor) {
        editor.destroy();
        setEditor(null);
      }
    };
  }, [editor]);

  // 处理右键菜单点击
  const handleMenuClick = useCallback(() => {
    setContextMenu(prev => ({ ...prev, visible: false }));
  }, []);

  // 获取文档类型选项
  const docTypeOptions = [
    { value: 'knowledge', label: '知识库' },
    { value: 'tutorial', label: '教程' },
    { value: 'document', label: '文档' },
    { value: 'other', label: '其他' },
  ];

  // 处理删除文档
  const handleDelete = (id: number) => {
    confirm({
      title: '确认删除',
      content: '确定要删除这个文档吗？删除后不可复。',
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          await documentApi.deleteDocument(id);
          message.success('删除成功');
          loadDocumentTree();
          if (selectedDoc?.id === id) {
            setSelectedDoc(undefined);
          }
        } catch (error: any) {
          message.error(error.message || '删除失败');
        }
      },
    });
  };

  // 添加临时节点
  const addTempNode = (parentId?: number) => {
    const tempId = `temp_${Date.now()}`;
    const tempNode: TempNode = {
      id: tempId as any,
      title: '',
      level: parentId ? 2 : 1,
      sort_order: 1,
      has_children: false,
      children: [],
      isTemp: true,
      parent_id: parentId,
    };

    if (parentId) {
      setTreeData(prevData => {
        const updateNodes = (nodes: TempNode[]): TempNode[] => {
          return nodes.map(node => {
            if (node.id === parentId) {
              return {
                ...node,
                has_children: true,
                children: [...(node.children || []), tempNode],
                expanded: true,
              };
            }
            if (node.children) {
              return {
                ...node,
                children: updateNodes(node.children),
              };
            }
            return node;
          });
        };
        return updateNodes(prevData);
      });
    } else {
      setTreeData(prevData => [...prevData, tempNode]);
    }
    setEditingKey(tempId);
    setEditingTitle('');
  };

  // 处理创建文档
  const handleCreate = async (tempId: string, parentId?: number) => {
    if (!editingTitle.trim()) {
      message.error('文档名称不能为空');
      return;
    }
    try {
      await documentApi.createDocument({
        title: editingTitle,
        content: '',
        parent_id: parentId,
      });
      message.success('创建成功');
      setEditingKey(null);
      loadDocumentTree();
    } catch (error: any) {
      message.error(error.message || '创建失败');
    }
  };

  // 处理重命名
  const handleRename = async (id: number) => {
    if (!editingTitle.trim()) {
      message.error('文档名称不能为空');
      return;
    }
    try {
      await documentApi.updateDocument(id, {
        title: editingTitle,
      });
      message.success('重命名成功');
      setEditingKey(null);
      loadDocumentTree();
      if (selectedDoc?.id === id) {
        loadDocument(id);
      }
    } catch (error: any) {
      message.error(error.message || '重命名失败');
    }
  };

  // 处理输入框失去焦点或回车
  const handleInputConfirm = (node: TempNode) => {
    if (!editingTitle.trim()) {
      if (node.isTemp) {
        setTreeData(prevData => {
          const removeNode = (nodes: TempNode[]): TempNode[] => {
            return nodes.filter(item => {
              if (item.children) {
                item.children = removeNode(item.children);
              }
              return item.id !== node.id;
            });
          };
          return removeNode(prevData);
        });
      }
    } else {
      if (node.isTemp) {
        handleCreate(node.id as unknown as string, node.parent_id);
      } else {
        handleRename(node.id as number);
      }
    }
    setEditingKey(null);
    setEditingTitle('');
  };

  // 右键菜单项
  const getContextMenuItems = (node: TempNode) => [
    {
      key: 'create',
      label: '新建文档',
      icon: <PlusOutlined />,
      onClick: () => addTempNode(node.id as number),
    },
    {
      key: 'rename',
      label: '重命名',
      icon: <EditOutlined />,
      onClick: () => {
        setEditingKey(node.id);
        setEditingTitle(node.title);
      },
    },
    {
      key: 'delete',
      label: '删除',
      icon: <DeleteOutlined />,
      danger: true,
      onClick: () => handleDelete(node.id as number),
    },
  ];

  // 转换树点数据，添加图标
  const convertTreeData = (nodes: TempNode[]): any[] => {
    return nodes.map(node => ({
      ...node,
      key: node.id,
      icon: node.has_children || (node.children && node.children.length > 0) ? <FolderOutlined /> : <FileOutlined />,
      children: node.children && node.children.length > 0 ? convertTreeData(node.children) : undefined,
      title: editingKey === node.id ? (
        <Input
          size="small"
          value={editingTitle}
          onChange={(e) => {
            e.stopPropagation();
            debouncedSetEditingTitle(e.target.value);
          }}
          onPressEnter={(e) => {
            e.stopPropagation();
            handleInputConfirm(node);
          }}
          onBlur={(e) => {
            e.stopPropagation();
            handleInputConfirm(node);
          }}
          autoFocus
          onClick={(e) => e.stopPropagation()}
          onKeyDown={(e) => {
            if (e.key === 'Escape') {
              e.stopPropagation();
              setEditingKey(null);
              setEditingTitle('');
              if (node.isTemp) {
                setTreeData(prevData => {
                  const removeNode = (nodes: TempNode[]): TempNode[] => {
                    return nodes.filter(item => {
                      if (item.children) {
                        item.children = removeNode(item.children);
                      }
                      return item.id !== node.id;
                    });
                  };
                  return removeNode(prevData);
                });
              }
            }
          }}
        />
      ) : node.title || '新建文档',
    }));
  };

  return (
    <div className={styles.container}>
      <div className={styles.sider}>
        <Card
          title="文档目录"
          extra={
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => addTempNode()}
            >
              新建文档
            </Button>
          }
        >
          <DirectoryTree
            treeData={convertTreeData(treeData)}
            onSelect={handleSelect}
            defaultExpandAll={false}
            showIcon
            onRightClick={({ event, node }) => {
              event.preventDefault();
              event.stopPropagation();
              setContextMenu({
                visible: true,
                x: event.clientX,
                y: event.clientY,
                node: node,
              });
            }}
          />
          {contextMenu.visible && contextMenu.node && (
            <div
              className={styles.contextMenu}
              style={{
                position: 'fixed',
                left: contextMenu.x,
                top: contextMenu.y,
                zIndex: 1050,
              }}
              onClick={(e) => e.stopPropagation()}
            >
              <Menu
                items={getContextMenuItems(contextMenu.node)}
                onClick={handleMenuClick}
              />
            </div>
          )}
        </Card>
      </div>
      <div className={styles.content}>
        
        <Card>
          {selectedDoc ? (
            <div className={styles.document}>
              <div className={styles.documentHeader}>
                <Title
                  level={4}
                  editable={{
                    onChange: handleTitleChange,
                    tooltip: '点击编辑标题',
                  }}
                >
                  {selectedDoc.title}
                </Title>
                <Button
                  type="link"
                  icon={<EyeOutlined />}
                  onClick={() => history.push(`/document/preview/${selectedDoc.id}`)}
                >
                  预览
                </Button>
              </div>
              <div className={styles.documentContent}>
                <div className={styles.editor}>
                  <Toolbar
                    editor={editor}
                    defaultConfig={toolbarConfig}
                    mode="default"
                    className={styles.toolbar}
                  />
                  <Editor
                    defaultConfig={editorConfig}
                    value={html}
                    onCreated={setEditor}
                    onChange={handleEditorChange}
                    mode="default"
                    className={styles.editorBody}
                    key={selectedDoc.id}
                  />
                </div>
              </div>
            </div>
          ) : (
            <div className={styles.empty}>
              <h3>请选择要查看的文档</h3>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default DocumentPage;