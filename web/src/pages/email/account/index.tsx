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
  PENDING: { color: 'default', text: '排队中' },
  RUNNING: { color: 'processing', text: '同步中' },
  COMPLETED: { color: 'success', text: '已同步' },
  FAILED: { color: 'error', text: '同步失败' },
  CANCELLED: { color: 'error', text: '已取消' },
  TIMEOUT: { color: 'error', text: '同步超时' },
};

const EmailAccountList: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [accounts, setAccounts] = useState<API.EmailAccount[]>([]);
  const [testingId, setTestingId] = useState<number>();
  const [syncingId, setSyncingId] = useState<number>();

  // 加载账列表
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

  // 同步件户
  const handleSync = async (id: number) => {
    try {
      setSyncingId(id);
      await emailApi.syncAccount(id);
      message.success('同步已开始，请稍后刷新查看结果');
      loadAccounts();
    } catch (error: any) {
      message.error(error.message || '同步失败');
    } finally {
      setSyncingId(undefined);
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
      width: '25%',
      render: (_, record) => (
        <div className={styles.accountCell}>
          <div className={styles.accountMain}>
            <a onClick={() => history.push(`/email/list/${record.id}`)}>{record.email_address}</a>
            {record.total_emails > 0 && (
              <Tag color="blue" className={styles.emailCount}>
                {record.total_emails}封邮件
              </Tag>
            )}
            <Button
              type="link"
              size="small"
              onClick={(e) => {
                e.stopPropagation();
                history.push(`/email/compose?account_id=${record.id}`);
              }}
            >
              写邮件
            </Button>
          </div>
          <div className={styles.accountStatus}>
            <Tag color={syncStatusConfig[record.sync_status].color}>
              {record.sync_status === 'SYNCING' && <SyncOutlined spin />}
              {syncStatusConfig[record.sync_status].text}
            </Tag>
            {record.last_sync_time && (
              <span className={styles.lastSync}>
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
      width: '20%',
      render: (_, record) => (
        <div className={styles.serverCell}>
          <div>{record.smtp_host}:{record.smtp_port}</div>
          {renderServerStatus(record, 'smtp')}
        </div>
      ),
    },
    {
      title: 'IMAP服务器',
      key: 'imap',
      width: '20%',
      render: (_, record) => (
        <div className={styles.serverCell}>
          <div>{record.imap_host}:{record.imap_port}</div>
          {renderServerStatus(record, 'imap')}
        </div>
      ),
    },
    {
      title: '同步状态',
      key: 'sync',
      width: '15%',
      render: (_, record) => (
        <Space>
          <Button
            size="small"
            onClick={() => handleSync(record.id)}
            loading={syncingId === record.id}
            disabled={record.sync_status === 'RUNNING'}
            icon={<SyncOutlined spin={record.sync_status === 'RUNNING'} />}
          >
            {record.sync_status === 'RUNNING' ? '同步中' : '同步'}
          </Button>
          <Button
            size="small"
            onClick={() => handleTest(record.id)}
            loading={testingId === record.id}
          >
            测试连接
          </Button>
        </Space>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: '15%',
      render: (_, record) => (
        <Space>
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