import React, { useState } from 'react';
import { Card } from 'antd';
import { emailApi } from '@/services/api/email';
import type { CreateEmailAccountParams } from '@/services/api/email';
import AccountForm from './components/AccountForm';
import styles from './index.less';

const CreateEmailAccount: React.FC = () => {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values: CreateEmailAccountParams) => {
    setLoading(true);
    try {
      await emailApi.createAccount(values);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Card title="新建邮件账户">
        <AccountForm onSubmit={handleSubmit} loading={loading} />
      </Card>
    </div>
  );
};

export default CreateEmailAccount; 