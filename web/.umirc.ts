import { defineConfig } from '@umijs/max';

export default defineConfig({
  antd: {},
  access: {},
  model: {},
  initialState: {},
  request: {},
  layout: {
    title: 'LLMRAGTools',
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
      name: '首页',
      icon: 'home',
      component: './dashboard',
    },
    {
      path: '/llm',
      name: 'LLM管理',
      icon: 'api',
      routes: [
        {
          path: '/llm/channel',
          name: '渠道管理',
          component: './llm/channel',
        },
        {
          path: '/llm/channel/create',
          name: '新建渠道',
          component: './llm/channel/create',
          hideInMenu: true,
        },
        {
          path: '/llm/channel/edit/:id',
          name: '编辑渠道',
          component: './llm/channel/edit',
          hideInMenu: true,
        },
        {
          path: '/llm/mapping',
          name: '功能映射',
          component: './llm/mapping',
        },
      ],
    },
    {
      path: '/document',
      name: '知识库',
      icon: 'book',
      routes: [
        {
          path: '/document',
          name: '文档管理',
          component: './document',
        },
        {
          path: '/document/create',
          name: '新建文档',
          component: './document/create',
          hideInMenu: true,
        },
        {
          path: '/document/edit/:id',
          name: '编辑文档',
          component: './document/edit',
          hideInMenu: true,
        },
        {
          path: '/document/preview/:id',
          name: '预览文档',
          component: './document/preview',
          hideInMenu: true,
        },
      ],
    },
    {
      path: '/email',
      name: '邮件功能',
      icon: 'mail',
      routes: [
        {
          path: '/email/account',
          name: '账户管理',
          component: './email/account',
        },
        {
          path: '/email/account/create',
          name: '新建账户',
          component: './email/account/create',
          hideInMenu: true,
        },
        {
          path: '/email/account/edit/:id',
          name: '编辑账户',
          component: './email/account/edit',
          hideInMenu: true,
        },
        {
          path: '/email/tag',
          name: '标签管理',
          component: './email/tag',
        },
        {
          path: '/email/list/:accountId',
          name: '邮件列表',
          component: './email/list',
          hideInMenu: true,
        },
        {
          path: '/email/list/:accountId/:emailId',
          name: '邮件详情',
          component: './email/list/detail',
          hideInMenu: true,
        },
        {
          path: '/email/compose',
          name: '写邮件',
          component: './email/compose',
          hideInMenu: true,
        },
        {
          path: '/email/outbox',
          name: '发件箱',
          component: './email/outbox',
        },
        {
          path: '/email/outbox/:emailId',
          name: '发件详情',
          component: './email/outbox/detail',
          hideInMenu: true,
        },
      ],
    },
    {
      name: '个人设置',
      icon: 'setting',
      path: '/account/settings',
      component: './account/settings',
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
      target: 'http://127.0.0.1:8111',
      changeOrigin: true,
      pathRewrite: { '^/api': '/api' },
    },
  },
  lessLoader: {
    modifyVars: {
      '@primary-color': '#1890ff',
    },
    javascriptEnabled: true,
  },
});

