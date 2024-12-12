import { apiRequest } from './request';
import { API_URLS } from './config';

export interface CreateEmailAccountParams {
  email_address: string;
  auth_token: string;
  smtp_host: string;
  smtp_port: number;
  imap_host: string;
  imap_port: number;
  use_ssl?: boolean;
  use_tls?: boolean;
}

export interface UpdateEmailAccountParams extends Partial<CreateEmailAccountParams> {}

export const emailApi = {
  // 获取邮件账户列表
  getAccounts: () => {
    return apiRequest<API.EmailAccount[]>(API_URLS.EMAIL.ACCOUNTS, {
      method: 'GET',
    });
  },

  // 获取邮件账户详情
  getAccount: (id: number) => {
    return apiRequest<API.EmailAccount>(`${API_URLS.EMAIL.ACCOUNTS}/${id}`, {
      method: 'GET',
    });
  },

  // 创建邮件账户
  createAccount: (params: CreateEmailAccountParams) => {
    return apiRequest<API.EmailAccount>(API_URLS.EMAIL.ACCOUNTS, {
      method: 'POST',
      data: params,
    });
  },

  // 更新邮件账户
  updateAccount: (id: number, params: UpdateEmailAccountParams) => {
    return apiRequest<API.EmailAccount>(`${API_URLS.EMAIL.ACCOUNTS}/${id}`, {
      method: 'PUT',
      data: params,
    });
  },

  // 删除邮件账户
  deleteAccount: (id: number) => {
    return apiRequest<void>(`${API_URLS.EMAIL.ACCOUNTS}/${id}`, {
      method: 'DELETE',
    });
  },

  // 获取邮件服务商列表
  getProviders: () => {
    return apiRequest<API.EmailProvider[]>(API_URLS.EMAIL.PROVIDERS, {
      method: 'GET',
    });
  },

  // 测试邮件账户连接
  testAccount: (id: number) => {
    return apiRequest<void>(`${API_URLS.EMAIL.ACCOUNTS}/${id}/test`, {
      method: 'POST',
    });
  },

  // 同步邮件账户
  syncAccount: (id: number) => {
    return apiRequest<void>(`${API_URLS.EMAIL.ACCOUNTS}/${id}/sync`, {
      method: 'POST',
    });
  },
}; 