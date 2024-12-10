import { defineConfig } from '@umijs/max';

export default defineConfig({
  antd: {},
  access: {},
  model: {},
  initialState: {},
  request: {},
  layout: false,
  routes: [
    {
      path: '/user',
      layout: false,
      routes: [
        { path: '/user/login', component: './user/login' },
        { path: '/user/register', component: './user/register' },
      ],
    },
    {
      path: '/',
      component: '@/layouts/BasicLayout',
      wrappers: ['@/wrappers/auth'],
      routes: [
        { path: '/', redirect: '/dashboard' },
        {
          path: '/dashboard',
          name: '仪表盘',
          component: './dashboard',
        },
      ],
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

