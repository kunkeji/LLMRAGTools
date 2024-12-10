import React, { useState } from 'react';
import { Card, Form, Input, Button, message, Upload, Avatar, Space } from 'antd';
import { UserOutlined, PhoneOutlined, LockOutlined, UploadOutlined } from '@ant-design/icons';
import { useModel } from '@umijs/max';
import type { RcFile, UploadProps } from 'antd/es/upload/interface';
import { userApi } from '@/services/api';
import { getApiUrl } from '@/config/config';
import styles from './index.less';

const AccountSettings: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const { initialState, refresh } = useModel('@@initialState');
  const { currentUser } = initialState || {};

  // 处理头像 URL
  const getAvatarUrl = (avatar?: string) => {
    if (!avatar) return undefined;
    return getApiUrl(avatar);
  };

  // 更新基本信息
  const handleUpdateProfile = async (values: any) => {
    try {
      setLoading(true);
      await userApi.updateProfile({
        nickname: values.nickname,
        phone_number: values.phone_number,
        password: values.password,
      });
      message.success('个人信息更新成功');
      refresh(); // 刷新用户信息
      form.resetFields(['password']); // 清空密码字段
    } catch (error: any) {
      message.error(error.message || '更新失败');
    } finally {
      setLoading(false);
    }
  };

  // 头像上传前的校验
  const beforeUpload = (file: RcFile) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
    if (!isJpgOrPng) {
      message.error('只能上传 JPG/PNG 格式的图片！');
      return false;
    }
    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
      message.error('图片大小不能超过 2MB！');
      return false;
    }
    return true;
  };

  // 处理头像上传
  const handleAvatarUpload: UploadProps['customRequest'] = async ({ file, onSuccess, onError }) => {
    try {
      setUploadLoading(true);
      const formData = new FormData();
      formData.append('file', file as File);
      await userApi.updateAvatar(file as File);
      message.success('头像更新成功');
      refresh(); // 刷新用户信息
      onSuccess?.('ok');
    } catch (error: any) {
      message.error(error.message || '头像上传失败');
      onError?.(error);
    } finally {
      setUploadLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Card bordered={false}>
        <div className={styles.avatarSection}>
          <Space size={16} align="center">
            <Avatar
              size={64}
              icon={<UserOutlined />}
              src={getAvatarUrl(currentUser?.avatar)}
            />
            <Upload
              name="file"
              showUploadList={false}
              beforeUpload={beforeUpload}
              customRequest={handleAvatarUpload}
            >
              <Button 
                icon={<UploadOutlined />} 
                loading={uploadLoading}
              >
                更换头像
              </Button>
            </Upload>
          </Space>
        </div>

        <div className={styles.formSection}>
          <Form
            form={form}
            layout="vertical"
            onFinish={handleUpdateProfile}
            initialValues={{
              nickname: currentUser?.nickname,
              phone_number: currentUser?.phone_number,
            }}
          >
            <Form.Item
              name="nickname"
              label="昵称"
              rules={[{ required: true, message: '请输入昵称！' }]}
            >
              <Input
                prefix={<UserOutlined />}
                placeholder="请输入昵称"
              />
            </Form.Item>

            <Form.Item
              name="phone_number"
              label="手机号码"
              rules={[
                { required: true, message: '请输入手机号码！' },
                { pattern: /^1\d{10}$/, message: '请输入有效的手机号码！' }
              ]}
            >
              <Input
                prefix={<PhoneOutlined />}
                placeholder="请输入手机号码"
              />
            </Form.Item>

            <Form.Item
              name="password"
              label="新密码"
              rules={[
                { min: 6, message: '密码长度不能小于6位！' }
              ]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="不修改请留空"
              />
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                loading={loading}
              >
                保存修改
              </Button>
            </Form.Item>
          </Form>
        </div>
      </Card>
    </div>
  );
};

export default AccountSettings;