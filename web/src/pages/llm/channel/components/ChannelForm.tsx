import React, { useState, useEffect } from 'react';
import { Form, Input, Select, Button, Space, message } from 'antd';
import { history } from '@umijs/max';
import { llmApi } from '@/services/api/llm';
import type { CreateChannelParams } from '@/services/api/llm';

interface ChannelFormProps {
  id?: number;
  onSubmit: (values: CreateChannelParams) => Promise<void>;
  loading?: boolean;
  initialValues?: Partial<API.LLMChannel>;
}

const ChannelForm: React.FC<ChannelFormProps> = ({
  id,
  onSubmit,
  loading,
  initialValues,
}) => {
  const [form] = Form.useForm();
  const [models, setModels] = useState<API.LLMModel[]>([]);
  const [loadingModels, setLoadingModels] = useState(false);

  // 加载模型列表
  useEffect(() => {
    const loadModels = async () => {
      try {
        setLoadingModels(true);
        const models = await llmApi.getModels();
        setModels(models || []);
      } catch (error) {
        console.error('加载模型列表失败:', error);
        message.error('加载模型列表失败');
      } finally {
        setLoadingModels(false);
      }
    };

    loadModels();
  }, []);

  // 获取可用的模型类型选项
  const modelTypeOptions = models.map(model => ({
    label: model.name,
    value: model.mapping_name,
    description: model.description,
  }));

  const handleSubmit = async (values: any) => {
    try {
      await onSubmit(values);
      message.success(id ? '更新成功' : '创建成功');
      history.push('/llm/channel');
    } catch (error: any) {
      message.error(error.message || (id ? '更新失败' : '创建失败'));
    }
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      initialValues={initialValues}
      style={{ maxWidth: 600 }}
    >
      <Form.Item
        name="channel_name"
        label="渠道名称"
        rules={[{ required: true, message: '请输入渠道名称' }]}
      >
        <Input placeholder="请输入渠道名称" />
      </Form.Item>

      <Form.Item
        name="model_type"
        label="模型类型"
        rules={[{ required: true, message: '请选择模型类型' }]}
        tooltip="选择要使用的 AI 模型提供商"
      >
        <Select
          placeholder="请选择模型类型"
          options={modelTypeOptions}
          loading={loadingModels}
          optionRender={(option) => (
            <Space direction="vertical" size={0}>
              <div>{option.data.label}</div>
              <div style={{ fontSize: '12px', color: '#666' }}>
                {option.data.description}
              </div>
            </Space>
          )}
        />
      </Form.Item>

      <Form.Item
        name="model"
        label="模型名称"
        rules={[{ required: true, message: '请输入模型名称' }]}
        tooltip="请输入想要使用的具体模型名称"
      >
        <Input placeholder="请输入模型名称，例如：chatglm_turbo" />
      </Form.Item>

      <Form.Item
        name="api_key"
        label="API密钥"
        rules={[{ required: true, message: '请输入API密钥' }]}
      >
        <Input.Password placeholder="请输入API密钥" />
      </Form.Item>

      <Form.Item
        name="proxy_url"
        label="代理地址"
        tooltip="可选，如果需要通过代理访问API，请填写代理地址"
      >
        <Input placeholder="请输入代理地址（可选）" />
      </Form.Item>

      <Form.Item>
        <Space>
          <Button type="primary" htmlType="submit" loading={loading}>
            {id ? '更新' : '创建'}
          </Button>
          <Button onClick={() => history.push('/llm/channel')}>取消</Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

export default ChannelForm; 