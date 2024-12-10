import { message } from 'antd';
import type { RequestConfig } from '@umijs/max';
import { history } from '@umijs/max';

// 错误处理方案：错误类型
enum ErrorShowType {
  SILENT = 0,
  WARN_MESSAGE = 1,
  ERROR_MESSAGE = 2,
  NOTIFICATION = 3,
  REDIRECT = 9,
}

// 与后端约定的响应数据格式
interface ResponseStructure {
  success: boolean;
  data: any;
  code?: string;
  message?: string;
  showType?: ErrorShowType;
}

// 运行时配置
export const request: RequestConfig = {
  // 统一的请求设置
  timeout: 10000,
  errorConfig: {
    errorHandler: (error: any) => {
      if (error.response) {
        // 请求成功发出且服务器也响应了状态码，但状态代码超出了 2xx 的范围
        message.error(`请求错误 ${error.response.status}: ${error.response.data.message}`);
      } else if (error.request) {
        // 请求已经成功发起，但没有收到响应
        message.error('网络错误，请检查网络连接');
      } else {
        // 发送请求时出了点问题
        message.error('请求失败，请稍后重试');
      }
      throw error;
    },
  },

  // 请求拦截器
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

  // 响应拦截器
  responseInterceptors: [
    (response: any) => {
      const { data } = response;
      if (data.code === '401') {
        localStorage.removeItem('access_token');
        history.push('/user/login');
        message.error('登录已过期，请重新登录');
      }
      return response;
    },
  ],
};

// 初始化状态
export async function getInitialState() {
  const token = localStorage.getItem('token');
  if (!token) {
    return {
      isLogin: false,
      currentUser: null,
    };
  }

  try {
    const response = await fetch('/api/users/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await response.json();

    if (response.ok) {
      return {
        isLogin: true,
        currentUser: data,
      };
    } else {
      localStorage.removeItem('token');
      return {
        isLogin: false,
        currentUser: null,
      };
    }
  } catch (error) {
    localStorage.removeItem('token');
    return {
      isLogin: false,
      currentUser: null,
    };
  }
}
