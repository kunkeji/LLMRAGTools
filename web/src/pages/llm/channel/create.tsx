import React, { useState } from 'react';
import { Card } from 'antd';
import { llmApi } from '@/services/api/llm';
import type { CreateChannelParams } from '@/services/api/llm';
import ChannelForm from './components/ChannelForm';
import styles from './index.less';

const CreateChannel: React.FC = () => {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values: CreateChannelParams) => {
    setLoading(true);
    try {
      await llmApi.createChannel(values);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Card title="新建渠道">
        <ChannelForm onSubmit={handleSubmit} loading={loading} />
      </Card>
    </div>
  );
};

export default CreateChannel; 