import React from 'react';
import { Card, Descriptions, Avatar, Row, Col, Statistic } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { useModel } from '@umijs/max';
import { getApiUrl } from '@/config/config';
import styles from './index.less';

const AccountCenter: React.FC = () => {
  const { initialState } = useModel('@@initialState');
  const { currentUser } = initialState || {};

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // 处理头像 URL
  const getAvatarUrl = (avatar?: string) => {
    if (!avatar) return undefined;
    return getApiUrl(avatar);
  };

  return (
    <div className={styles.container}>
      <Card bordered={false}>
        <div className={styles.avatarHolder}>
          <Avatar
            size={104}
            icon={<UserOutlined />}
            src={getAvatarUrl(currentUser?.avatar)}
          />
          <div className={styles.name}>{currentUser?.nickname || currentUser?.username}</div>
          <div className={styles.detail}>{currentUser?.email}</div>
        </div>

        <div className={styles.detail}>
          <Descriptions title="基本信息" column={2}>
            <Descriptions.Item label="用户名">{currentUser?.username}</Descriptions.Item>
            <Descriptions.Item label="邮箱">{currentUser?.email}</Descriptions.Item>
            <Descriptions.Item label="昵称">{currentUser?.nickname || '-'}</Descriptions.Item>
            <Descriptions.Item label="手机号码">{currentUser?.phone_number || '-'}</Descriptions.Item>
            <Descriptions.Item label="注册时间">
              {currentUser?.created_at ? formatDate(currentUser.created_at) : '-'}
            </Descriptions.Item>
            <Descriptions.Item label="最后更新">
              {currentUser?.updated_at ? formatDate(currentUser.updated_at) : '-'}
            </Descriptions.Item>
          </Descriptions>
        </div>
      </Card>

      <Row gutter={24} className={styles.statisticRow}>
        <Col span={8}>
          <Card>
            <Statistic title="代理总数" value={0} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="在线代理" value={0} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="本月流量" value={0} suffix="GB" />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default AccountCenter;