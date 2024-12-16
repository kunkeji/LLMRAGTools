import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, message, Modal, Form, Input, ColorPicker } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { emailApi } from '@/services/api/email';
import type { EmailTag } from '@/services/api/email';
import styles from './index.less';

const EmailTagPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [tags, setTags] = useState<EmailTag[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTag, setEditingTag] = useState<EmailTag | null>(null);
  const [form] = Form.useForm();

  // 加载标签列表
  const loadTags = async () => {
    try {
      setLoading(true);
      const data = await emailApi.getTags();
      setTags(data);
    } catch (error: any) {
      message.error(error.message || '加载标签失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTags();
  }, []);

  // 打开创建/编辑模态框
  const showModal = (tag?: EmailTag) => {
    setEditingTag(tag || null);
    if (tag) {
      form.setFieldsValue({
        name: tag.name,
        color: tag.color,
        description: tag.description,
      });
    } else {
      form.resetFields();
    }
    setModalVisible(true);
  };

  // 处理表单提交
  const handleSubmit = async (values: { name: string; color: string; description: string }) => {
    values.color = `#${values.color.metaColor.r.toString(16).padStart(2, '0')}${values.color.metaColor.g.toString(16).padStart(2, '0')}${values.color.metaColor.b.toString(16).padStart(2, '0')}`;
    try {
      if (editingTag) {
        await emailApi.updateTag(editingTag.id, values);
        message.success('标签更新成功');
      } else {
        await emailApi.createTag(values);
        message.success('标签创建成功');
      }
      setModalVisible(false);
      loadTags();
    } catch (error: any) {
      message.error(error.message || '操作失败');
    }
  };

  // 处理删除标签
  const handleDelete = (tag: EmailTag) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个标签吗？删除后不可恢复。',
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          await emailApi.deleteTag(tag.id);
          message.success('删除成功');
          loadTags();
        } catch (error: any) {
          message.error(error.message || '删除失败');
        }
      },
    });
  };

  const columns = [
    {
      title: '标签名称',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: EmailTag) => (
        <Space>
          <div
            style={{
              width: 16,
              height: 16,
              borderRadius: 4,
              backgroundColor: record.color,
              marginRight: 8,
            }}
          />
          {text}
        </Space>
      ),
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (text: string) => new Date(text).toLocaleString(),
    },
    {
      title: '更新时间',
      dataIndex: 'updated_at',
      key: 'updated_at',
      render: (text: string) => new Date(text).toLocaleString(),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: EmailTag) => (
        <Space>
          <Button
            type="text"
            icon={<EditOutlined />}
            onClick={() => showModal(record)}
          >
            编辑
          </Button>
          <Button
            type="text"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record)}
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
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => showModal()}
          >
            新建标签
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={tags}
          rowKey="id"
          loading={loading}
        />
      </Card>

      <Modal
        title={editingTag ? '编辑标签' : '新建标签'}
        open={modalVisible}
        onOk={() => form.submit()}
        onCancel={() => {
          setModalVisible(false);
          setEditingTag(null);
          form.resetFields();
        }}
      >
        <Form
          form={form}
          onFinish={handleSubmit}
          layout="vertical"
        >
          <Form.Item
            name="name"
            label="标签名称"
            rules={[{ required: true, message: '请输入标签名称' }]}
          >
            <Input placeholder="请输入标签名称" />
          </Form.Item>
          <Form.Item
            name="description"
            label="标签描述"
          >
            <Input.TextArea placeholder="请输入标签描述" />
          </Form.Item>
          <Form.Item
            name="color"
            label="标签颜色"
            rules={[{ required: true, message: '请选择标签颜色' }]}
          >
            <ColorPicker />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default EmailTagPage; 