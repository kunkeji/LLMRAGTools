import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, message, Tag, Input, Select, Modal, Dropdown, Menu, Popover, ColorPicker, Tooltip } from 'antd';
import { SearchOutlined, StarOutlined, StarFilled, DeleteOutlined, FolderOutlined, TagOutlined, PlusOutlined, EditOutlined } from '@ant-design/icons';
import { useParams, history } from '@umijs/max';
import { emailApi } from '@/services/api/email';
import type { ColumnsType } from 'antd/es/table';
import type { EmailTag } from '@/services/api/email';
import styles from './index.less';

const { confirm } = Modal;
const { Option } = Select;

const EmailList: React.FC = () => {
  const { accountId } = useParams<{ accountId: string }>();
  const [loading, setLoading] = useState(false);
  const [emails, setEmails] = useState<API.Email[]>([]);
  const [searchText, setSearchText] = useState('');
  const [folder, setFolder] = useState<string>('INBOX');
  const [isRead, setIsRead] = useState<boolean | undefined>();
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });
  const [tags, setTags] = useState<EmailTag[]>([]);
  const [tagModalVisible, setTagModalVisible] = useState(false);
  const [editingTag, setEditingTag] = useState<EmailTag | null>(null);
  const [tagName, setTagName] = useState('');
  const [tagColor, setTagColor] = useState('#1890ff');

  // 加载邮件列表
  const loadEmails = async (page = pagination.current, pageSize = pagination.pageSize) => {
    if (!accountId) return;
    try {
      setLoading(true);
      const data = await emailApi.getEmails(parseInt(accountId), {
        folder,
        is_read: isRead,
        skip: (page - 1) * pageSize,
        limit: pageSize,
      });
      
      setEmails(data.items || []);
      setPagination({
        current: data.page,
        pageSize: data.size,
        total: data.total,
      });
    } catch (error: any) {
      message.error(error.message || '加载邮件列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEmails(1);
  }, [accountId, folder, isRead]);

  // 处理表格分页变化
  const handleTableChange = (newPagination: any) => {
    loadEmails(newPagination.current, newPagination.pageSize);
  };

  // 标记已读/未读
  const handleMarkRead = async (emailId: number, isRead: boolean) => {
    if (!accountId) return;
    try {
      await emailApi.markEmailRead(parseInt(accountId), emailId, isRead);
      message.success(isRead ? '已标记为已读' : '已标记为未读');
      loadEmails();
    } catch (error: any) {
      message.error(error.message || '操作失败');
    }
  };

  // 删除邮件
  const handleDelete = (emailId: number) => {
    if (!accountId) return;
    confirm({
      title: '确认删除',
      content: '确定要删除这封邮件吗？',
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          await emailApi.deleteEmail(parseInt(accountId), emailId);
          message.success('删除成功');
          loadEmails();
        } catch (error: any) {
          message.error(error.message || '删除失败');
        }
      },
    });
  };

  // 处理邮件点击
  const handleEmailClick = async (record: API.Email) => {
    try {
      // 如果邮件未读,标记为已读
      if (!record.is_read) {
        await handleMarkRead(record.id, true);
      }
      // 跳转到邮件详情页
      history.push(`/email/list/${accountId}/${record.id}`);
    } catch (error) {
      console.error('处理邮件点击失败:', error);
    }
  };


  // 邮件标签菜单
  const emailTagMenu = (email: API.Email) => (
    <Menu>
      {tags.map(tag => (
        <Menu.Item
          key={tag.id}
          onClick={() => handleEmailTag(email.id, tag.id, email.tags?.some(t => t.id === tag.id))}
        >
          <Space>
            <Tag color={tag.color}>{tag.name}</Tag>
            {email.tags?.some(t => t.id === tag.id) && <span style={{ color: '#52c41a' }}>✓</span>}
          </Space>
        </Menu.Item>
      ))}
    </Menu>
  );

  // 更新表格列配置
  const columns: ColumnsType<API.Email> = [
    // {
    //   title: '操作',
    //   key: 'action',
    //   width: 120,
    //   fixed: 'left',
    //   render: (_, record) => (
    //     <Space>
    //       <Dropdown overlay={emailTagMenu(record)} trigger={['click']}>
    //         <Button
    //           type="text"
    //           icon={<TagOutlined />}
    //           onClick={(e) => e.stopPropagation()}
    //         />
    //       </Dropdown>
    //       <Button
    //         type="text"
    //         icon={record.is_flagged ? <StarFilled style={{ color: '#faad14' }} /> : <StarOutlined />}
    //         onClick={(e) => {
    //           e.stopPropagation();
    //           handleMarkFlagged(record.id, !record.is_flagged);
    //         }}
    //       />
    //       <Button
    //         type="text"
    //         danger
    //         icon={<DeleteOutlined />}
    //         onClick={(e) => {
    //           e.stopPropagation();
    //           handleDelete(record.id);
    //         }}
    //       />
    //     </Space>
    //   ),
    // },
    {
      title: '发件人',
      key: 'from',
      width: 220,
      render: (_, record) => (
        <div>
          <div>{record.from_name || record.from_address}</div>
          {record.from_name && (
            <div className={styles.fromAddress}>{record.from_address}</div>
          )}
          <div className={styles.emailTime}>
            {new Date(record.date).toLocaleString()}
          </div>
        </div>
      ),
    },
    {
      title: '主题',
      dataIndex: 'subject',
      key: 'subject',
      render: (text, record) => (
        <div className={styles.subjectCell}>
          <Space size={4} wrap className={styles.tags}>
            {record.tags?.map(tag => (
              <Tag key={tag.id} color={tag.color}>{tag.name}</Tag>
            ))}
            {!record.is_read && <Tag color="blue">未读</Tag>}
          </Space>
          <div className={styles.subject}>{text}</div>
        </div>
      ),
    },
  ];

  return (
    <div className={styles.container}>
      <Card>
        <div className={styles.toolbar}>
          <Space>
            <Input
              placeholder="搜索邮件"
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              style={{ width: 200 }}
            />
            <Select
              value={folder}
              onChange={(value) => {
                setFolder(value);
                setPagination(prev => ({ ...prev, current: 1 }));
              }}
              style={{ width: 120 }}
            >
              <Option value="INBOX">收件箱</Option>
              <Option value="SENT">已发送</Option>
              <Option value="DRAFT">草稿箱</Option>
              <Option value="TRASH">垃圾箱</Option>
              <Option value="ARCHIVE">归档</Option>
            </Select>
            <Select
              value={isRead}
              onChange={(value) => {
                setIsRead(value);
                setPagination(prev => ({ ...prev, current: 1 }));
              }}
              style={{ width: 120 }}
              allowClear
              placeholder="阅读状态"
            >
              <Option value={true}>已读</Option>
              <Option value={false}>未读</Option>
            </Select>
          </Space>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => history.push(`/email/compose?account_id=${accountId}`)}
          >
            写邮件
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={emails}
          rowKey="id"
          loading={loading}
          pagination={{
            ...pagination,
            showQuickJumper: true,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 条`,
          }}
          onChange={handleTableChange}
          onRow={(record) => ({
            onClick: () => handleEmailClick(record),
            style: { cursor: 'pointer' },
          })}
        />
      </Card>
    </div>
  );
};

export default EmailList; 