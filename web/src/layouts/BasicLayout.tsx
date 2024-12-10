import React from 'react';
import { Layout, Menu, Dropdown, Avatar } from 'antd';
import { useLocation, history } from '@umijs/max';
import {
  UserOutlined,
  LogoutOutlined,
  DashboardOutlined,
} from '@ant-design/icons';
import styles from './BasicLayout.less';

const { Header, Content, Sider } = Layout;

const menuItems = [
  {
    key: '/dashboard',
    icon: <DashboardOutlined />,
    label: '仪表盘',
  },
];

const BasicLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    history.push('/user/login');
  };

  const userMenu = (
    <Menu>
      <Menu.Divider />
      <Menu.Item key="logout" onClick={handleLogout}>
        <LogoutOutlined /> 退出登录
      </Menu.Item>
    </Menu>
  );

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header className={styles.header}>
        <div className={styles.logo}>代理工具平台</div>
        <div className={styles.right}>
          <Dropdown overlay={userMenu} placement="bottomRight">
            <span className={styles.action}>
              <Avatar size="small" icon={<UserOutlined />} />
              <span className={styles.name}>用户名</span>
            </span>
          </Dropdown>
        </div>
      </Header>
      <Layout>
        <Sider width={200} className={styles.sider}>
          <Menu
            mode="inline"
            selectedKeys={[location.pathname]}
            style={{ height: '100%', borderRight: 0 }}
            items={menuItems}
            onClick={({ key }) => history.push(key)}
          />
        </Sider>
        <Layout style={{ padding: '24px' }}>
          <Content className={styles.content}>{children}</Content>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default BasicLayout;