import { request } from '@umijs/max';
import { message } from 'antd';
import { history } from '@umijs/max';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  data?: any;
  params?: Record<string, any>;
  headers?: Record<string, string>;
  requestType?: 'form' | 'json';
}

export async function apiRequest<T>(url: string, options: RequestOptions = {}): Promise<T> {
  try {
    const { method = 'GET', data, params, headers = {}, requestType } = options;

    // 添加认证头
    const token = localStorage.getItem('access_token');
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const requestOptions: any = {
      method,
      headers,
    };

    // 处理请求数据
    if (data) {
      if (data instanceof FormData) {
        requestOptions.data = data;
      } else if (requestType === 'form') {
        const formData = new FormData();
        Object.entries(data).forEach(([key, value]) => {
          formData.append(key, value as string);
        });
        requestOptions.data = formData;
        requestOptions.requestType = 'form';
      } else {
        requestOptions.data = data;
      }
    }

    // 处理URL参数
    if (params) {
      requestOptions.params = params;
    }

    const response = await request<API.Response<T>>(url, requestOptions);
    
    // 处理响应
    if (response.code === '200') {
      return response.data;
    } else if (response.code === '401') {
      // token 失效，清除 token 并跳转到登录页
      localStorage.removeItem('access_token');
      const currentPath = window.location.pathname;
      history.push(`/user/login?redirect=${encodeURIComponent(currentPath)}`);
      throw new Error('登录已过期，请重新登录');
    } else {
      throw new Error(response.message || '请求失败');
    }
  } catch (error: any) {
    // 如果是 401 错误，不显示错误消息（因为已经在上面处理了）
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      const currentPath = window.location.pathname;
      history.push(`/user/login?redirect=${encodeURIComponent(currentPath)}`);
      throw new Error('登录已过期，请重新登录');
    }
    
    if (error.message !== '登录已过期，请重新登录') {
      message.error(error.message || '请求失败');
    }
    throw error;
  }
} 