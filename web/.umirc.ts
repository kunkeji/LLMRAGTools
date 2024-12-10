import { defineConfig } from '@umijs/max';

export default defineConfig({
  antd: {},
  access: {},
  model: {},
  initialState: {},
  request: {},
  layout: {
    title: '代理工具平台',
    locale: false,
  },
  routes: [
    {
      path: '/user',
      layout: false,
      routes: [
        { path: '/user/login', component: './user/login' },
        { path: '/user/register', component: './user/register' },
        { path: '/user/forgot-password', component: './user/forgot-password' },
      ],
    },
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/dashboard',
      name: '仪表盘',
      icon: 'dashboard',
      component: './dashboard',
    },
    {
      path: '*',
      layout: false,
      component: './404',
    },
  ],
  fastRefresh: true,
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8112',
      changeOrigin: true,
    },
  },
  lessLoader: {
    modifyVars: {
      '@primary-color': '#1890ff',
    },
    javascriptEnabled: true,
  },
});

