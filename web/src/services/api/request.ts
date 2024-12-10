import { request } from '@umijs/max';
import { message } from 'antd';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  data?: any;
  params?: Record<string, any>;
  headers?: Record<string, string>;
  requestType?: 'form' | 'json';
}

export async function apiRequest<T>(url: string, options: RequestOptions = {}): Promise<T> {
  try {
    const { method = 'GET', data, params, headers, requestType } = options;

    const requestOptions: any = {
      method,
      headers: {
        ...headers,
      },
    };

    // 处理请求数据
    if (data) {
      if (requestType === 'form') {
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

    // 添加认证头
    const token = localStorage.getItem('access_token');
    if (token) {
      requestOptions.headers.Authorization = `Bearer ${token}`;
    }

    const response = await request<API.Response<T>>(url, requestOptions);
    
    if (response.code === '200') {
      return response.data;
    } else {
      throw new Error(response.message);
    }
  } catch (error: any) {
    message.error(error.message || '请求失败');
    throw error;
  }
} 