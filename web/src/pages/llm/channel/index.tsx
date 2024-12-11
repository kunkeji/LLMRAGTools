import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Modal, message, Input, Tag } from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
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

  const columns: ColumnsType<API.LLMChannel> = [
    {
      title: '渠道名称',
      dataIndex: 'channel_name',
      key: 'channel_name',
      width: 200,
    },
    {
      title: '模型类型',
      dataIndex: 'model_type',
      key: 'model_type',
      width: 120,
      render: (text: string) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: '模型',
      dataIndex: 'model',
      key: 'model',
      width: 120,
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
      render: (text: string) => new Date(text).toLocaleString(),
    },
    {
      title: '操作',
      key: 'action',
      width: 180,
      render: (_, record) => (
        <Space>
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