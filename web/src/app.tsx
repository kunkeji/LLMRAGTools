import React from 'react';
import { message } from 'antd';
import type { RequestConfig, RunTimeLayoutConfig } from '@umijs/max';
import { history } from '@umijs/max';
import { userApi } from '@/services/api';
import { AvatarDropdown } from '@/components/RightContent';

const loginPath = '/user/login';

// 请求配置
export const request: RequestConfig = {
  timeout: 10000,
  errorConfig: {
    errorHandler: (error: any) => {
      if (error.response?.status === 401) {
        localStorage.removeItem('access_token');
        history.push(loginPath);
        message.error('登录已过期，请重新登录');
      } else if (error.response) {
        message.error(`请求错误: ${error.response.data.message || '未知错误'}`);
      } else if (error.request) {
        message.error('网络错误，请检查网络连接');
      } else {
        message.error('请求失败，请稍后重试');
      }
      throw error;
    },
  },

  requestInterceptors: [
    (config: any) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers = {
          ...config.headers,
          Authorization: `Bearer ${token}`,
        };
      }
      return config;
    },
  ],

  responseInterceptors: [
    (response: any) => {
      const { data } = response;
      if (data?.code === '401') {
        localStorage.removeItem('access_token');
        history.push(loginPath);
        message.error('登录已过期，请重新登录');
      }
      return response;
    },
  ],
};

// 初始化状态
export async function getInitialState() {
  const token = localStorage.getItem('access_token');
  if (!token) {
    return {
      isLogin: false,
      currentUser: null,
    };
  }

  try {
    const currentUser = await userApi.getCurrentUser();
    return {
      isLogin: true,
      currentUser,
    };
  } catch (error) {
    localStorage.removeItem('access_token');
    return {
      isLogin: false,
      currentUser: null,
    };
  }
}

// 运行时布局配置
export const layout: RunTimeLayoutConfig = ({ initialState, setInitialState }) => {
  return {
    logo: 'https://img.alicdn.com/tfs/TB1YHEpwUT1gK0jSZFhXXaAtVXa-28-27.svg',
    title: '代理工具平台',
    layout: 'mix',
    splitMenus: false,
    menu: {
      locale: false,
    },
    rightContentRender: () => <AvatarDropdown />,
    logout: async () => {
      await setInitialState({
        isLogin: false,
        currentUser: null,
      });
      localStorage.removeItem('access_token');
      history.push(loginPath);
    },
    hideInMenu: ['/user/login', '/user/register'],
    hideInBreadcrumb: ['/user/login', '/user/register'],
    waterMarkProps: {
      content: '',
    },
    // 未登录时重定向到登录页
    onPageChange: () => {
      const { location } = history;
      if (!initialState?.currentUser && location.pathname !== loginPath) {
        history.push(loginPath);
      }
    },
  };
}; 