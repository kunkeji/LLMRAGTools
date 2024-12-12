import React, { useState, useEffect } from 'react';
import { Card, Spin, message } from 'antd';
import { useParams } from '@umijs/max';
import { emailApi } from '@/services/api/email';
import type { UpdateEmailAccountParams } from '@/services/api/email';
import AccountForm from './components/AccountForm';
import styles from './index.less';

const EditEmailAccount: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [account, setAccount] = useState<API.EmailAccount>();

  useEffect(() => {
    const loadAccount = async () => {
      if (!id) return;
      try {
        setLoading(true);
        const data = await emailApi.getAccount(parseInt(id));
        setAccount(data);
      } catch (error) {
        console.error('加载邮件账户信息失败:', error);
        message.error('加载邮件账户信息失败');
      } finally {
        setLoading(false);
      }
    };

    loadAccount();
  }, [id]);

  const handleSubmit = async (values: UpdateEmailAccountParams) => {
    if (!id) return;
    setSubmitting(true);
    try {
      await emailApi.updateAccount(parseInt(id), values);
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
      <Card title="编辑邮件账户">
        <AccountForm
          id={parseInt(id!)}
          onSubmit={handleSubmit}
          loading={submitting}
          initialValues={account}
        />
      </Card>
    </div>
  );
};

export default EditEmailAccount; 