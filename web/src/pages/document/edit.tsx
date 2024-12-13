import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Select, Button, Space, message, Spin } from 'antd';
import { useParams, history } from '@umijs/max';
import { documentApi } from '@/services/api/document';
import type { DocumentUpdateParams } from '@/services/api/document';
import styles from './index.less';

const { TextArea } = Input;

const EditDocument: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [document, setDocument] = useState<API.Document>();

  // 加载文档信息
  useEffect(() => {
    const loadDocument = async () => {
      if (!id) return;
      try {
        setLoading(true);
        const data = await documentApi.getDocument(parseInt(id));
        setDocument(data);
        form.setFieldsValue(data);
      } catch (error: any) {
        message.error(error.message || '加载文档失败');
      } finally {
        setLoading(false);
      }
    };

    loadDocument();
  }, [id, form]);

  const handleSubmit = async (values: DocumentUpdateParams) => {
    if (!id) return;
    try {
      setSubmitting(true);
      await documentApi.updateDocument(parseInt(id), values);
      message.success('更新成功');
      history.push('/document');
    } catch (error: any) {
      message.error(error.message || '更新失败');
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
      <Card title="编辑文档">
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          style={{ maxWidth: 800 }}
        >
          <Form.Item
            name="title"
            label="标题"
            rules={[{ required: true, message: '请输入文档标题' }]}
          >
            <Input placeholder="请输入文档标题" />
          </Form.Item>

          <Form.Item
            name="doc_type"
            label="文档类型"
            tooltip="选择文档的类型，便于分类管理"
          >
            <Select
              placeholder="请选择文档类型"
              allowClear
              options={[
                { label: '知识库', value: 'knowledge' },
                { label: '教程', value: 'tutorial' },
                { label: '文档', value: 'document' },
                { label: '其他', value: 'other' },
              ]}
            />
          </Form.Item>

          <Form.Item
            name="content"
            label="内容"
            rules={[{ required: true, message: '请输入文档内容' }]}
          >
            <TextArea
              placeholder="请输入文档内容"
              autoSize={{ minRows: 10, maxRows: 20 }}
            />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={submitting}>
                更新
              </Button>
              <Button onClick={() => history.push('/document')}>取消</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default EditDocument; 