import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Modal, message, Tag, Tooltip } from 'antd';
import { PlusOutlined, SyncOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { history } from '@umijs/max';
import { emailApi } from '@/services/api/email';
import type { ColumnsType } from 'antd/es/table';
import styles from './index.less';

const { confirm } = Modal;

// 同步状态配置
const syncStatusConfig = {
  NEVER: { color: 'default', text: '未同步' },
  SYNCING: { color: 'processing', text: '同步中' },
  SUCCESS: { color: 'success', text: '已同步' },
  ERROR: { color: 'error', text: '同步失败' },
};

const EmailAccountList: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [accounts, setAccounts] = useState<API.EmailAccount[]>([]);
  const [testingId, setTestingId] = useState<number>();

  // 加载账户列表
  const loadAccounts = async () => {
    try {
      setLoading(true);
      const data = await emailApi.getAccounts();
      setAccounts(data || []);
    } catch (error: any) {
      if (error.message !== '登录已过期，请重新登录') {
        message.error('加载邮件账户列表失败');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAccounts();
  }, []);

  // 删除账户
  const handleDelete = (id: number) => {
    confirm({
      title: '确认删除',
      content: '确定要删除这个邮件账户吗？删除后不可恢复。',
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          await emailApi.deleteAccount(id);
          message.success('删除成功');
          loadAccounts();
        } catch (error) {
          console.error('删除邮件账户失败:', error);
        }
      },
    });
  };

  // 测试账户连接
  const handleTest = async (id: number) => {
    try {
      setTestingId(id);
      await emailApi.testAccount(id);
      message.success('测试已开始，请稍后刷新查看结果');
      loadAccounts();
    } catch (error: any) {
      message.error(error.message || '测试失败');
    } finally {
      setTestingId(undefined);
    }
  };

  // 渲染服务器状态
  const renderServerStatus = (record: API.EmailAccount, type: 'smtp' | 'imap') => {
    const lastTestTime = type === 'smtp' ? record.smtp_last_test_time : record.imap_last_test_time;
    const testResult = type === 'smtp' ? record.smtp_test_result : record.imap_test_result;
    const testError = type === 'smtp' ? record.smtp_test_error : record.imap_test_error;

    return (
      <div style={{ marginTop: 4 }}>
        {lastTestTime ? (
          <Tooltip title={testError || `最后测试: ${new Date(lastTestTime).toLocaleString()}`}>
            <Tag color={testResult ? 'success' : 'error'}>
              {testResult ? <CheckCircleOutlined /> : <CloseCircleOutlined />}
              {testResult ? '连接正常' : '连接异常'}
            </Tag>
          </Tooltip>
        ) : (
          <Tag>未测试</Tag>
        )}
      </div>
    );
  };

  const columns: ColumnsType<API.EmailAccount> = [
    {
      title: '邮箱账户',
      key: 'account',
      width: '30%',
      render: (_, record) => (
        <div>
          <div style={{ fontSize: '14px', marginBottom: 4 }}>{record.email_address}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            <Tag color={syncStatusConfig[record.sync_status].color}>
              {record.sync_status === 'SYNCING' && <SyncOutlined spin />}
              {syncStatusConfig[record.sync_status].text}
            </Tag>
            {record.last_sync_time && (
              <span style={{ marginLeft: 8 }}>
                最后同步: {new Date(record.last_sync_time).toLocaleString()}
              </span>
            )}
          </div>
        </div>
      ),
    },
    {
      title: 'SMTP服务器',
      key: 'smtp',
      width: '30%',
      render: (_, record) => (
        <div>
          <div>{record.smtp_host}:{record.smtp_port}</div>
          {renderServerStatus(record, 'smtp')}
        </div>
      ),
    },
    {
      title: 'IMAP服务器',
      key: 'imap',
      width: '30%',
      render: (_, record) => (
        <div>
          <div>{record.imap_host}:{record.imap_port}</div>
          {renderServerStatus(record, 'imap')}
        </div>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: '10%',
      render: (_, record) => (
        <Space direction="vertical" size="small">
          <Button
            type="link"
            size="small"
            onClick={() => handleTest(record.id)}
            loading={testingId === record.id}
          >
            测试连接
          </Button>
          <Button
            type="link"
            size="small"
            onClick={() => history.push(`/email/account/edit/${record.id}`)}
          >
            编辑
          </Button>
          <Button
            type="link"
            size="small"
            danger
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
          <div />
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => history.push('/email/account/create')}
          >
            新建账户
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={accounts}
          rowKey="id"
          loading={loading}
          pagination={{
            showQuickJumper: true,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 条`,
          }}
        />
      </Card>
    </div>
  );
};

export default EmailAccountList; 