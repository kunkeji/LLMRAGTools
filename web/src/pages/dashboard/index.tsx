import React, { useState, useEffect } from 'react';
import { Card, Typography, Descriptions } from 'antd';
import { userApi } from '@/services/api';
import styles from './index.less';

const { Title, Paragraph } = Typography;

const DashboardPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [userInfo, setUserInfo] = useState<API.CurrentUser | null>(null);

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        setLoading(true);
        const data = await userApi.getCurrentUser();
        setUserInfo(data);
      } catch (error) {
        console.error('获取用户信息失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserInfo();
  }, []);

  return (
    <div className={styles.container}>
      <Card loading={loading}>
        <Title level={2}>欢迎使用代理工具平台</Title>
        <Paragraph>
          这是一个简单的仪表盘页面，显示了您的基本信息。
        </Paragraph>

        {userInfo && (
          <Descriptions title="用户信息" column={2}>
            <Descriptions.Item label="用户名">{userInfo.username}</Descriptions.Item>
            <Descriptions.Item label="邮箱">{userInfo.email}</Descriptions.Item>
            <Descriptions.Item label="状态">{userInfo.status === 'active' ? '正常' : '禁用'}</Descriptions.Item>
            <Descriptions.Item label="注册时间">
              {new Date(userInfo.created_at).toLocaleString()}
            </Descriptions.Item>
          </Descriptions>
        )}
      </Card>
    </div>
  );
};

export default DashboardPage; 