import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, message, Tag, Input, Select, Modal } from 'antd';
import { SearchOutlined, StarOutlined, StarFilled, DeleteOutlined, FolderOutlined } from '@ant-design/icons';
import { useParams, history } from '@umijs/max';
import { emailApi } from '@/services/api/email';
import type { ColumnsType } from 'antd/es/table';
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

  // 标记重要/取消重要
  const handleMarkFlagged = async (emailId: number, isFlagged: boolean) => {
    if (!accountId) return;
    try {
      await emailApi.markEmailFlagged(parseInt(accountId), emailId, isFlagged);
      message.success(isFlagged ? '已标记为重要' : '已取消重要标记');
      loadEmails();
    } catch (error: any) {
      message.error(error.message || '操作失败');
    }
  };

  // 移动到文件夹
  const handleMove = async (emailId: number, targetFolder: string) => {
    if (!accountId) return;
    try {
      await emailApi.moveEmail(parseInt(accountId), emailId, targetFolder);
      message.success('移���成功');
      loadEmails();
    } catch (error: any) {
      message.error(error.message || '移动失败');
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

  const columns: ColumnsType<API.Email> = [
    {
      title: '发件人',
      key: 'from',
      width: 200,
      render: (_, record) => (
        <div>
          <div>{record.from_name || record.from_address}</div>
          {record.from_name && (
            <div style={{ fontSize: '12px', color: '#666' }}>{record.from_address}</div>
          )}
        </div>
      ),
    },
    {
      title: '主题',
      dataIndex: 'subject',
      key: 'subject',
      render: (text, record) => (
        <div>
          {!record.is_read && <Tag color="blue">未读</Tag>}
          {text}
        </div>
      ),
    },
    {
      title: '时间',
      dataIndex: 'date',
      key: 'date',
      width: 180,
      render: (text) => new Date(text).toLocaleString(),
    },
    {
      title: '操作',
      key: 'action',
      width: 180,
      render: (_, record) => (
        <Space>
          <Button
            type="text"
            icon={record.is_flagged ? <StarFilled style={{ color: '#faad14' }} /> : <StarOutlined />}
            onClick={(e) => {
              e.stopPropagation();
              handleMarkFlagged(record.id, !record.is_flagged);
            }}
          />
          <Button
            type="text"
            icon={<FolderOutlined />}
            onClick={(e) => {
              e.stopPropagation();
              handleMove(record.id, 'Archive');
            }}
          />
          <Button
            type="text"
            danger
            icon={<DeleteOutlined />}
            onClick={(e) => {
              e.stopPropagation();
              handleDelete(record.id);
            }}
          />
        </Space>
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