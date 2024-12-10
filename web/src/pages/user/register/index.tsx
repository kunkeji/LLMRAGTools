import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons';
import { history, Link } from 'umi';
import { userApi } from '@/services/api';
import styles from './index.less';

const RegisterPage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [sendingCode, setSendingCode] = useState(false);
  const [countdown, setCountdown] = useState(0);

  const startCountdown = () => {
    setCountdown(60);
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const handleSendCode = async () => {
    try {
      const email = form.getFieldValue('email');
      if (!email) {
        message.error('请输入邮箱地址');
        return;
      }
      setSendingCode(true);
      await userApi.sendVerificationCode({
        email,
        purpose: 'register',
      });
      message.success('验证码已发送');
      startCountdown();
    } catch (error: any) {
      // 错误处理已经在 apiRequest 中统一处理
    } finally {
      setSendingCode(false);
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      await userApi.register({
        email: values.email,
        username: values.username,
        password: values.password,
        verification_code: values.verification_code,
      });
      message.success('注册成功');
      history.push('/user/login');
    } catch (error: any) {
      // 错误处理已经在 apiRequest 中统一处理
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.top}>
          <div className={styles.header}>
            <h1>代理工具平台</h1>
          </div>
          <div className={styles.desc}>专业的代理管理工具</div>
        </div>

        <div className={styles.main}>
          <Form
            form={form}
            name="register"
            onFinish={handleSubmit}
          >
            <Form.Item
              name="email"
              rules={[
                { required: true, message: '请输入邮箱！' },
                { type: 'email', message: '请输入有效的邮箱地址！' },
              ]}
            >
              <Input
                prefix={<MailOutlined />}
                placeholder="邮箱"
                size="large"
              />
            </Form.Item>

            <Form.Item
              name="username"
              rules={[{ required: true, message: '请输入用户名！' }]}
            >
              <Input
                prefix={<UserOutlined />}
                placeholder="用户名"
                size="large"
              />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[{ required: true, message: '请输入密码！' }]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="密码"
                size="large"
              />
            </Form.Item>

            <Form.Item
              name="verification_code"
              rules={[{ required: true, message: '请输入验证码！' }]}
            >
              <div style={{ display: 'flex', gap: '8px' }}>
                <Input
                  placeholder="验证码"
                  size="large"
                />
                <Button
                  size="large"
                  loading={sendingCode}
                  disabled={countdown > 0}
                  onClick={handleSendCode}
                >
                  {countdown > 0 ? `${countdown}s` : '获取验证码'}
                </Button>
              </div>
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                size="large"
                block
                loading={loading}
              >
                注册
              </Button>
            </Form.Item>

            <div className={styles.other}>
              <Link to="/user/login">返回登录</Link>
            </div>
          </Form>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage; 