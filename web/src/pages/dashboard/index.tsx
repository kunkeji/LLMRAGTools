import React from 'react';
import { Card, Typography } from 'antd';
import styles from './index.less';

const { Title, Paragraph } = Typography;

const DashboardPage: React.FC = () => {
  return (
    <div className={styles.container}>
      <Card>
        <Title level={2}>欢迎使用代理工具平台</Title>
        <Paragraph>
          这是一个简单的仪表盘页面。更多功能正在开发中...
        </Paragraph>
      </Card>
    </div>
  );
};

export default DashboardPage; 