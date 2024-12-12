import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Modal, message, Input, Tag, Tooltip } from 'antd';
import { PlusOutlined, SearchOutlined, CheckCircleOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import { history } from '@umijs/max';
import { llmApi } from '@/services/api/llm';
import type { ColumnsType } from 'antd/es/table';
import styles from './index.less';

const { confirm } = Modal;

const ChannelList: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [channels, setChannels] = useState<API.LLMChannel[]>([]);
  const [keyword, setKeyword] = useState('');
  const [modelType, setModelType] = useState<string>();
  const [testingId, setTestingId] = useState<number>();

  // 加载渠道列表
  const loadChannels = async () => {
    try {
      setLoading(true);
      const data = await llmApi.getChannels({
        keyword,
        model_type: modelType,
      });
      setChannels(data || []);
    } catch (error: any) {
      // 如果不是登录过期的错误，才显示错误信息
      if (error.message !== '登录已过期，请重新登录') {
        message.error('加载渠道列表失败');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadChannels();
  }, [keyword, modelType]);

  // 删除渠道
  const handleDelete = (id: number) => {
    confirm({
      title: '确认删除',
      content: '确定要删除这个渠道吗？删除后不可恢复。',
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          await llmApi.deleteChannel(id);
          message.success('删除成功');
          loadChannels();
        } catch (error) {
          console.error('删除渠道失败:', error);
        }
      },
    });
  };

  // 测试渠道
  const handleTest = async (id: number) => {
    try {
      setTestingId(id);
      await llmApi.testChannel(id);
      message.success('测试成功，渠道可用');
      loadChannels(); // 刷新列表以获取最新的响应时间
    } catch (error: any) {
      message.error(error.message || '测试失败，请检查配置');
    } finally {
      setTestingId(undefined);
    }
  };

  // 格式化响应时间
  const formatResponseTime = (ms?: number) => {
    if (!ms) return '-';
    return `${ms.toFixed(0)}ms`;
  };

  // 格式化测试时间
  const formatTestTime = (time?: string) => {
    if (!time) return '-';
    return new Date(time).toLocaleString();
  };

  const columns: ColumnsType<API.LLMChannel> = [
    {
      title: '渠道名称',
      dataIndex: 'channel_name',
      key: 'channel_name',
      width: 180,
    },
    {
      title: '模型类型',
      dataIndex: 'model_type',
      key: 'model_type',
      width: 100,
      render: (text: string) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: '模型',
      dataIndex: 'model',
      key: 'model',
      width: 120,
    },
    {
      title: '响应时间',
      key: 'response_time',
      width: 200,
      render: (_, record) => (
        <Space direction="vertical" size={0}>
          <div>
            最近: {formatResponseTime(record.last_response_time)}
            {record.last_test_time && (
              <Tooltip title={`最后测试时间: ${formatTestTime(record.last_test_time)}`}>
                <span style={{ marginLeft: 8, fontSize: 12, color: '#666' }}>
                  {record.test_count ? `(${record.test_count}次)` : ''}
                </span>
              </Tooltip>
            )}
          </div>
          <div style={{ fontSize: 12, color: '#666' }}>
            平均: {formatResponseTime(record.avg_response_time)}
            {record.min_response_time && record.max_response_time && (
              <Tooltip title={`最小: ${formatResponseTime(record.min_response_time)}\n最大: ${formatResponseTime(record.max_response_time)}`}>
                <span style={{ marginLeft: 4 }}>
                  <ExclamationCircleOutlined />
                </span>
              </Tooltip>
            )}
          </div>
        </Space>
      ),
    },
    // {
    //   title: '创建时间',
    //   dataIndex: 'created_at',
    //   key: 'created_at',
    //   width: 180,
    //   render: (text: string) => new Date(text).toLocaleString(),
    // },
    {
      title: '操作',
      key: 'action',
      width: 250,
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            onClick={() => handleTest(record.id)}
            loading={testingId === record.id}
          >
            测试
          </Button>
          <Button
            type="link"
            onClick={() => history.push(`/llm/channel/edit/${record.id}`)}
          >
            编辑
          </Button>
          <Button
            type="link"
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
          <Space>
            <Input
              placeholder="搜索渠道名称"
              allowClear
              prefix={<SearchOutlined />}
              onChange={(e) => setKeyword(e.target.value)}
              style={{ width: 200 }}
            />
          </Space>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => history.push('/llm/channel/create')}
          >
            新建渠道
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={channels}
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

export default ChannelList; 