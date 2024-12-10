import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { history, Link } from '@umijs/max';
import { userApi } from '@/services/api';
import styles from './index.less';

const LoginPage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      const data = await userApi.login({
        username: values.username,
        password: values.password,
      });
      localStorage.setItem('access_token', data.access_token);
      message.success('登录成功');
      history.push('/dashboard');
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
              <Link to="/user/register">注册账号</Link>
            </div>
          </Form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage; 