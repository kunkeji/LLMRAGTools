import React, { useState, useEffect } from 'react';
import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { history, useModel } from '@umijs/max';
import { userApi } from '@/services/api';
import styles from './index.less';

const LoginPage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const { refresh } = useModel('@@initialState');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      history.push('/');
    }
  }, []);

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      const data = await userApi.login({
        username: values.username,
        password: values.password,
      });
      localStorage.setItem('access_token', data.access_token);
      message.success('登录成功');
      
      // 刷新用户信息
      await refresh();
      
      // 获取重定向地址
      const urlParams = new URL(window.location.href).searchParams;
      const redirect = urlParams.get('redirect');
      history.push(redirect || '/dashboard');
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
            <h1>大语言模型插件式框架</h1>
          </div>
          <div className={styles.desc}>专业的大语言模型插件式框架</div>
        </div>

        <div className={styles.main}>
          <Form
            form={form}
            name="login"
            onFinish={handleSubmit}
          >
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

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                size="large"
                block
                loading={loading}
              >
                登录
              </Button>
            </Form.Item>

            <div className={styles.other}>
              <a href="/user/register">注册账号</a>
              <a href="/user/forgot-password">忘记密码</a>
            </div>
          </Form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage; 