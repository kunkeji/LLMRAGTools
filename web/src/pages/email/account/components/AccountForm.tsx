import React, { useState, useEffect } from 'react';
import { Form, Input, Button, Space, message, AutoComplete, Switch, Modal } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import { history } from '@umijs/max';
import { emailApi } from '@/services/api/email';
import type { CreateEmailAccountParams } from '@/services/api/email';

interface AccountFormProps {
  id?: number;
  onSubmit: (values: CreateEmailAccountParams) => Promise<void>;
  loading?: boolean;
  initialValues?: Partial<API.EmailAccount>;
}

const AccountForm: React.FC<AccountFormProps> = ({
  id,
  onSubmit,
  loading,
  initialValues,
}) => {
  const [form] = Form.useForm();
  const [providers, setProviders] = useState<API.EmailProvider[]>([]);
  const [loadingProviders, setLoadingProviders] = useState(false);
  const [emailOptions, setEmailOptions] = useState<{ value: string; provider?: API.EmailProvider }[]>([]);
  const [isCustom, setIsCustom] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState<API.EmailProvider | null>(null);

  // 加载服务商列表
  useEffect(() => {
    const loadProviders = async () => {
      try {
        setLoadingProviders(true);
        const data = await emailApi.getProviders();
        setProviders(data || []);
      } catch (error) {
        console.error('加载服务商列表失败:', error);
        message.error('加载服务商列表失败');
      } finally {
        setLoadingProviders(false);
      }
    };

    loadProviders();
  }, []);

  // 处理邮箱地址变化
  const handleEmailChange = (value: string) => {
    if (!value) {
      setEmailOptions([]);
      return;
    }

    // 获取@后面的域名部分
    const atIndex = value.indexOf('@');
    if (atIndex === -1) {
      // 如果还没有输入@，显示所有服务商的域名建议
      const options = [
        ...providers.map(provider => ({
          value: `${value}${provider.domain_suffix}`,
          provider,
        })),
        {
          value: `${value}@`,
          label: '自定义邮箱服务器',
          isCustom: true,
        },
      ];
      setEmailOptions(options);
    } else {
      const domain = value.slice(atIndex);
      // 根据已输入的域名筛选匹配的服务商
      const matchedOptions = providers
        .filter(provider => provider.domain_suffix.startsWith(domain))
        .map(provider => ({
          value: `${value.slice(0, atIndex)}${provider.domain_suffix}`,
          provider,
        }));
      
      // 添加自定义选项
      const options = [
        ...matchedOptions,
        {
          value: value,
          label: '自定义邮箱服务器',
          isCustom: true,
        },
      ];
      setEmailOptions(options);
    }
  };

  // 处理选择邮箱地址
  const handleEmailSelect = (_: string, option: any) => {
    if (option.isCustom) {
      setIsCustom(true);
      setSelectedProvider(null);
      form.setFieldsValue({
        smtp_host: '',
        smtp_port: 465,
        imap_host: '',
        imap_port: 993,
        use_ssl: true,
        use_tls: false,
      });
    } else if (option.provider) {
      setIsCustom(false);
      setSelectedProvider(option.provider);
      const { provider } = option;
      form.setFieldsValue({
        smtp_host: provider.smtp_host,
        smtp_port: provider.smtp_port,
        imap_host: provider.imap_host,
        imap_port: provider.imap_port,
        use_ssl: provider.use_ssl,
        use_tls: provider.use_tls,
      });
    }
  };

  // 显示服务器配置信息
  const showServerConfig = () => {
    if (!selectedProvider) return;

    Modal.info({
      title: `${selectedProvider.name}服务器配置`,
      content: (
        <div>
          <p>SMTP服务器：{selectedProvider.smtp_host}</p>
          <p>SMTP端口：{selectedProvider.smtp_port}</p>
          <p>IMAP服务器：{selectedProvider.imap_host}</p>
          <p>IMAP端口：{selectedProvider.imap_port}</p>
          <p>SSL：{selectedProvider.use_ssl ? '是' : '否'}</p>
          <p>TLS：{selectedProvider.use_tls ? '是' : '否'}</p>
          {selectedProvider.description && (
            <p>说明：{selectedProvider.description}</p>
          )}
          {selectedProvider.help_url && (
            <p>
              <a href={selectedProvider.help_url} target="_blank" rel="noopener noreferrer">
                查看帮助文档
              </a>
            </p>
          )}
        </div>
      ),
      width: 500,
    });
  };

  const handleSubmit = async (values: any) => {
    try {
      // 确保所有服务器配置都被提交
      const submitData = {
        display_name: values.display_name,
        email_address: values.email_address,
        auth_token: values.auth_token,
        smtp_host: isCustom ? values.smtp_host : selectedProvider?.smtp_host,
        smtp_port: isCustom ? parseInt(values.smtp_port) : selectedProvider?.smtp_port,
        imap_host: isCustom ? values.imap_host : selectedProvider?.imap_host,
        imap_port: isCustom ? parseInt(values.imap_port) : selectedProvider?.imap_port,
        use_ssl: isCustom ? values.use_ssl : selectedProvider?.use_ssl,
        use_tls: isCustom ? values.use_tls : selectedProvider?.use_tls,
      };

      await onSubmit(submitData);
      message.success(id ? '更新成功' : '创建成功');
      history.push('/email/account');
    } catch (error: any) {
      message.error(error.message || (id ? '更新失败' : '创建失败'));
    }
  };

  // 如果是编辑模式，显示所有服务器配置
  useEffect(() => {
    if (id && initialValues) {
      setIsCustom(true);
    }
  }, [id, initialValues]);

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      initialValues={{
        ...initialValues,
        use_ssl: initialValues?.use_ssl ?? true,
        use_tls: initialValues?.use_tls ?? false,
      }}
      style={{ maxWidth: 600 }}
    >
      <Form.Item
        name="display_name"
        label="名称"
      >
        <Input placeholder="请输入名称,作为发件时对方可以显示的名称" />
      </Form.Item>

      <Form.Item
        name="email_address"
        label={
          <Space>
            邮箱地址
            {selectedProvider && (
              <InfoCircleOutlined 
                style={{ cursor: 'pointer', color: '#1890ff' }}
                onClick={showServerConfig}
              />
            )}
          </Space>
        }
        rules={[
          { required: true, message: '请输入邮箱地址' },
          { type: 'email', message: '请输入有效的邮箱地址' },
        ]}
      >
        <AutoComplete
          options={emailOptions}
          onChange={handleEmailChange}
          onSelect={handleEmailSelect}
          placeholder="请输入邮箱地址"
          defaultActiveFirstOption
          disabled={!!id}  // 编辑模式下禁用邮箱地址修改
        />
      </Form.Item>

      <Form.Item
        name="auth_token"
        label="授权码"
        rules={[{ required: true, message: '请输入授权码' }]}
        tooltip="请输入邮箱的授权码，不是登录密码"
      >
        <Input.Password placeholder="请输入授权码" />
      </Form.Item>

      {/* 编辑模式或自定义模式下显示服务器配置 */}
      {(isCustom || id) && (
        <>
          <Form.Item
            name="smtp_host"
            label="SMTP服务器地址"
            rules={[{ required: true, message: '请输入SMTP服务器地址' }]}
          >
            <Input placeholder="请输入SMTP服务器地址" />
          </Form.Item>

          <Form.Item
            name="smtp_port"
            label="SMTP端口"
            rules={[{ required: true, message: '请输入SMTP端口' }]}
          >
            <Input type="number" placeholder="请输入SMTP端口" />
          </Form.Item>

          <Form.Item
            name="imap_host"
            label="IMAP服务器地址"
            rules={[{ required: true, message: '请输入IMAP服务器地址' }]}
          >
            <Input placeholder="请输入IMAP服务器地址" />
          </Form.Item>

          <Form.Item
            name="imap_port"
            label="IMAP端口"
            rules={[{ required: true, message: '请输入IMAP端口' }]}
          >
            <Input type="number" placeholder="请输入IMAP端口" />
          </Form.Item>

          <Form.Item
            name="use_ssl"
            label="使用SSL"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            name="use_tls"
            label="使用TLS"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>
        </>
      )}

      <Form.Item>
        <Space>
          <Button type="primary" htmlType="submit" loading={loading}>
            {id ? '更新' : '创建'}
          </Button>
          <Button onClick={() => history.push('/email/account')}>取消</Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

export default AccountForm; 