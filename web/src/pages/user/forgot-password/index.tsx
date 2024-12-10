import React, { useState, useEffect } from 'react';
import { Form, Input, Button, message, Steps } from 'antd';
import { MailOutlined, LockOutlined, SafetyOutlined } from '@ant-design/icons';
import { history } from '@umijs/max';
import { userApi } from '@/services/api';
import styles from './index.less';

const { Step } = Steps;

const ForgotPasswordPage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [email, setEmail] = useState('');
  const [countdown, setCountdown] = useState(0);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      history.push('/');
    }
  }, []);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (countdown > 0) {
      timer = setTimeout(() => setCountdown(countdown - 1), 1000);
    }
    return () => {
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, [countdown]);

  const handleSendCode = async () => {
    try {
      const values = await form.validateFields(['email']);
      setLoading(true);
      await userApi.sendResetPasswordCode({
        email: values.email,
        purpose: 'reset_password'
      });
      setEmail(values.email);
      message.success('验证码已发送到您的邮箱');
      setCountdown(60);
      setCurrentStep(1);
    } catch (error: any) {
      if (error.name === 'ValidationError') {
        return;
      }
      message.error(error.message || '发送验证码失败');
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (values: any) => {
    try {
      setLoading(true);
      await userApi.resetPassword({
        email: email,
        code: values.code,
        new_password: values.password
      });
      message.success('密码重置成功，请重新登录');
      history.push('/user/login');
    } catch (error: any) {
      message.error(error.message || '重置密码失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.top}>
          <div className={styles.header}>
            <h1>忘记密码</h1>
          </div>
          <div className={styles.desc}>重置您的账户密码</div>
        </div>

        <div className={styles.main}>
          <Steps current={currentStep} className={styles.steps}>
            <Step title="验证邮箱" />
            <Step title="重置密码" />
          </Steps>

          <Form
            form={form}
            onFinish={currentStep === 0 ? handleSendCode : handleResetPassword}
            className={styles.form}
          >
            {currentStep === 0 ? (
              <Form.Item
                name="email"
                rules={[
                  { required: true, message: '请输入邮箱地址！' },
                  { type: 'email', message: '请输入有效的邮箱地址！' }
                ]}
              >
                <Input
                  prefix={<MailOutlined />}
                  placeholder="请输入注册邮箱"
                  size="large"
                />
              </Form.Item>
            ) : (
              <>
                <Form.Item
                  name="code"
                  rules={[
                    { required: true, message: '请输入验证码！' },
                    { len: 6, message: '验证码长度应为6位！' }
                  ]}
                >
                  <Input
                    prefix={<SafetyOutlined />}
                    placeholder="请输入验证码"
                    size="large"
                    maxLength={6}
                    addonAfter={
                      <Button
                        type="link"
                        disabled={countdown > 0}
                        onClick={handleSendCode}
                        style={{ padding: 0 }}
                      >
                        {countdown > 0 ? `${countdown}秒后重新发送` : '重新发送'}
                      </Button>
                    }
                  />
                </Form.Item>

                <Form.Item
                  name="password"
                  rules={[
                    { required: true, message: '请输入新密码！' },
                    { min: 6, message: '密码长度不能小于6位！' }
                  ]}
                >
                  <Input.Password
                    prefix={<LockOutlined />}
                    placeholder="请输入新密码"
                    size="large"
                  />
                </Form.Item>

                <Form.Item
                  name="confirmPassword"
                  dependencies={['password']}
                  rules={[
                    { required: true, message: '请确认新密码！' },
                    ({ getFieldValue }) => ({
                      validator(_, value) {
                        if (!value || getFieldValue('password') === value) {
                          return Promise.resolve();
                        }
                        return Promise.reject(new Error('两次输入的密码不一致！'));
                      },
                    }),
                  ]}
                >
                  <Input.Password
                    prefix={<LockOutlined />}
                    placeholder="请确认新密码"
                    size="large"
                  />
                </Form.Item>
              </>
            )}

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                size="large"
                block
                loading={loading}
              >
                {currentStep === 0 ? '发送验证码' : '重置密码'}
              </Button>
            </Form.Item>

            <div className={styles.other}>
              <a href="/user/login">返回登录</a>
            </div>
          </Form>
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;