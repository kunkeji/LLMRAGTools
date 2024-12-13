import React, { useState, useEffect } from 'react';
import { Card, Spin, message, Button } from 'antd';
import { useParams, history } from '@umijs/max';
import { documentApi } from '@/services/api/document';
import { ArrowLeftOutlined } from '@ant-design/icons';
import '@wangeditor/editor/dist/css/style.css';
import styles from './preview.less';

const PreviewPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [loading, setLoading] = useState(false);
  const [document, setDocument] = useState<API.Document>();

  useEffect(() => {
    const loadDocument = async () => {
      if (!id) return;
      try {
        setLoading(true);
        const data = await documentApi.getDocument(parseInt(id));
        setDocument(data);
      } catch (error: any) {
        message.error(error.message || '加载文档失败');
      } finally {
        setLoading(false);
      }
    };

    loadDocument();
  }, [id]);

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
      <Card>
        <div className={styles.document}>
          <div className={styles.documentHeader}>
            <Button
              type="link"
              icon={<ArrowLeftOutlined />}
              onClick={() => history.back()}
              className={styles.backButton}
            >
              返回编辑
            </Button>
            <h1>{document?.title}</h1>
          </div>
          <div className={styles.documentContent}>
            <div
              className={styles.content}
              dangerouslySetInnerHTML={{ __html: document?.content || '' }}
            />
          </div>
        </div>
      </Card>
    </div>
  );
};

export default PreviewPage; 