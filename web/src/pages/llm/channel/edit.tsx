import React, { useState, useEffect } from 'react';
import { Card, Spin, message } from 'antd';
import { useParams } from '@umijs/max';
import { llmApi } from '@/services/api/llm';
import type { UpdateChannelParams } from '@/services/api/llm';
import ChannelForm from './components/ChannelForm';
import styles from './index.less';

const EditChannel: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [channel, setChannel] = useState<API.LLMChannel>();

  useEffect(() => {
    const loadChannel = async () => {
      if (!id) return;
      try {
        setLoading(true);
        const data = await llmApi.getChannel(parseInt(id));
        setChannel(data);
      } catch (error) {
        console.error('加载渠道信息失败:', error);
        message.error('加载渠道信息失败');
      } finally {
        setLoading(false);
      }
    };

    loadChannel();
  }, [id]);

  const handleSubmit = async (values: UpdateChannelParams) => {
    if (!id) return;
    setSubmitting(true);
    try {
      await llmApi.updateChannel(parseInt(id), values);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <Card>
          <div style={{ textAlign: 'center', padding: '50px 0' }}>
            <Spin />
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Card title="编辑渠道">
        <ChannelForm
          id={parseInt(id!)}
          onSubmit={handleSubmit}
          loading={submitting}
          initialValues={channel}
        />
      </Card>
    </div>
  );
};

export default EditChannel; 