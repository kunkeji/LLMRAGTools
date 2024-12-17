import React, { useState, useEffect } from 'react';
import { Card, Table, Space, message, Tag, Input, Select, Button, Modal, DatePicker } from 'antd';
import { SearchOutlined, DeleteOutlined, RedoOutlined } from '@ant-design/icons';
import { history } from '@umijs/max';
import { emailApi } from '@/services/api/email';
import type { ColumnsType } from 'antd/es/table';
import styles from './index.less';

const { Option } = Select;
const { RangePicker } = DatePicker;

// 添加状态类型
type EmailStatus = 'draft' | 'pending' | 'sent' | 'failed';

// 添加回复类型
type ReplyType = 'pre_reply' | 'auto_reply' | 'manual_reply' | 'quick_reply';

const EmailOutboxList: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [emails, setEmails] = useState<API.EmailOutbox[]>([]);
  const [accounts, setAccounts] = useState<API.EmailAccount[]>([]);
  const [selectedAccount, setSelectedAccount] = useState<number>();
  const [searchText, setSearchText] = useState('');
  const [status, setStatus] = useState<EmailStatus>();
  const [replyType, setReplyType] = useState<ReplyType>();
  const [dateRange, setDateRange] = useState<[string, string]>();
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });



  // 加载邮件账户列表
  useEffect(() => {
    const loadAccounts = async () => {
      try {
        const data = await emailApi.getAccounts();
        setAccounts(data);
        if (data.length > 0) {
          setSelectedAccount(data[0].id);
        }
      } catch (error: any) {
        message.error(error.message || '加载邮件账户失败');
      }
    };
    loadAccounts();
  }, []);

  // 加载发件箱列表
const loadEmails = async (page = pagination.current, pageSize = pagination.pageSize) => {
    try {
      setLoading(true);
      const params: any = {
        skip: (page - 1) * pageSize,
        limit: pageSize,
        account_id: selectedAccount,
        status,
        reply_type: replyType,
        search: searchText,
      };
  
      if (dateRange) {
        params.start_date = dateRange[0];
        params.end_date = dateRange[1];
      }
  
      const data = await emailApi.getOutboxList(params);
      // 直接使用返回的数据数组
      setEmails(data || []);
      setPagination({
        current: page,
        pageSize,
        total: data.length, // 使用数组长度作为总数
      });
    } catch (error: any) {
      message.error(error.message || '加载邮件列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedAccount) {
      loadEmails(1);
    }
  }, [selectedAccount, status, replyType, searchText, dateRange]);

  // 处理格分页变化
  const handleTableChange = (newPagination: any) => {
    loadEmails(newPagination.current, newPagination.pageSize);
  };

  // 删除邮件
  const handleDelete = (emailId: number) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这封邮件吗？',
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          await emailApi.deleteOutboxEmail(emailId);
          message.success('删除成功');
          loadEmails();
        } catch (error: any) {
          message.error(error.message || '删除失败');
        }
      },
    });
  };

  // 重新发送
  const handleResend = async (emailId: number) => {
    try {
      await emailApi.resendEmail(emailId);
      message.success('已重新发送');
      loadEmails();
    } catch (error: any) {
      message.error(error.message || '重新发送失败');
    }
  };

  // 获取状态标签配置
  const getStatusConfig = (status: EmailStatus) => {
    const config: Record<EmailStatus, { color: string; text: string }> = {
      draft: { color: 'default', text: '草稿' },
      pending: { color: 'processing', text: '发送中' },
      sent: { color: 'success', text: '已发送' },
      failed: { color: 'error', text: '发送失败' },
    };
    return config[status] || { color: 'default', text: status };
  };

  // 获取回复类型显示文本
  const getReplyTypeText = (type?: ReplyType) => {
    const types: Record<ReplyType, string> = {
      pre_reply: '预设回复',
      auto_reply: '自动回复',
      manual_reply: '手动回复',
      quick_reply: '快速回复',
    };
    return type ? types[type] || type : '-';
  };

  // 处理邮件点击
  const handleEmailClick = (record: API.EmailOutbox) => {
    history.push(`/email/outbox/${record.id}`);
  };

  const columns: ColumnsType<API.EmailOutbox> = [
    {
      title: '收件人',
      dataIndex: 'recipients',
      key: 'recipients',
      width: 200,
    },
    {
      title: '主题',
      dataIndex: 'subject',
      key: 'subject',
      width: 300,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      render: (status: EmailStatus) => {
        const config = getStatusConfig(status);
        return <Tag color={config.color}>{config.text}</Tag>;
      },
    },
    {
      title: '回复类型',
      dataIndex: 'reply_type',
      key: 'reply_type',
      width: 120,
      render: (type?: ReplyType) => getReplyTypeText(type),
    },
    {
      title: '发送时间',
      dataIndex: 'send_time',
      key: 'send_time',
      width: 180,
      render: (time?: string) => time ? new Date(time).toLocaleString() : '-',
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space>
          {record.status === 'failed' && (
            <Button
              type="link"
              icon={<RedoOutlined />}
              onClick={() => handleResend(record.id)}
            >
              重新发送
            </Button>
          )}
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
          >
            删除
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div className={styles.container}>
      <Card>
        <div className={styles.toolbar}>
          <Space wrap>
            <Select
              value={selectedAccount}
              onChange={setSelectedAccount}
              style={{ width: 200 }}
              placeholder="选择邮件账户"
            >
              {accounts.map(account => (
                <Option key={account.id} value={account.id}>
                  {account.email_address}
                </Option>
              ))}
            </Select>
            <Input
              placeholder="搜索邮件"
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              style={{ width: 200 }}
            />
            <Select
              value={status}
              onChange={setStatus}
              style={{ width: 120 }}
              allowClear
              placeholder="发送状态"
            >
              <Option value="draft">草稿</Option>
              <Option value="pending">发送中</Option>
              <Option value="sent">已发送</Option>
              <Option value="failed">发送失败</Option>
            </Select>
            <Select
              value={replyType}
              onChange={setReplyType}
              style={{ width: 120 }}
              allowClear
              placeholder="回复类型"
            >
              <Option value="pre_reply">预设回复</Option>
              <Option value="auto_reply">自动回复</Option>
              <Option value="manual_reply">手动回复</Option>
              <Option value="quick_reply">快速回复</Option>
            </Select>
            <RangePicker
              onChange={(dates) => {
                if (dates) {
                  setDateRange([
                    dates[0]!.format('YYYY-MM-DD'),
                    dates[1]!.format('YYYY-MM-DD'),
                  ]);
                } else {
                  setDateRange(undefined);
                }
              }}
            />
          </Space>
          <Button
            type="primary"
            onClick={() => history.push(`/email/compose?account_id=${selectedAccount}`)}
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

export default EmailOutboxList; 