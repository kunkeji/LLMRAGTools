import React, { useState } from 'react';
import { Card, Form, Input, Select, Button, Space, message } from 'antd';
import { history, useLocation } from '@umijs/max';
import { documentApi } from '@/services/api/document';
import type { DocumentCreateParams } from '@/services/api/document';
import styles from './index.less';

const { TextArea } = Input;

const CreateDocument: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const parentId = searchParams.get('parent_id');

  const handleSubmit = async (values: DocumentCreateParams) => {
    try {
      setLoading(true);
      await documentApi.createDocument({
        ...values,
        parent_id: parentId ? parseInt(parentId) : undefined,
      });
      message.success('创建成功');
      history.push('/document');
    } catch (error: any) {
      message.error(error.message || '创建失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Card title="新建文档">
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
              <Button type="primary" htmlType="submit" loading={loading}>
                创建
              </Button>
              <Button onClick={() => history.push('/document')}>取消</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default CreateDocument; 