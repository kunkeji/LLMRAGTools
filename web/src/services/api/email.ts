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

export interface GetEmailsParams {
  folder?: string;
  is_read?: boolean;
  is_flagged?: boolean;
  skip?: number;
  limit?: number;
  order_by?: string;
  order_desc?: boolean;
}

export interface UpdateEmailParams {
  is_read?: boolean;
  is_flagged?: boolean;
  folder?: string;
  importance?: number;
}

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

  // 获取邮件列表
  getEmails: (accountId: number, params?: GetEmailsParams) => {
    return apiRequest<API.Email[]>(`${API_URLS.EMAIL.ACCOUNTS}/${accountId}/emails`, {
      method: 'GET',
      params,
    });
  },

  // 获取邮件详情
  getEmail: (accountId: number, emailId: number) => {
    return apiRequest<API.Email>(`${API_URLS.EMAIL.ACCOUNTS}/${accountId}/emails/${emailId}`, {
      method: 'GET',
    });
  },

  // 更新邮件
  updateEmail: (accountId: number, emailId: number, params: UpdateEmailParams) => {
    return apiRequest<API.Email>(`${API_URLS.EMAIL.ACCOUNTS}/${accountId}/emails/${emailId}`, {
      method: 'PUT',
      data: params,
    });
  },

  // 删除邮件
  deleteEmail: (accountId: number, emailId: number, permanent: boolean = false) => {
    return apiRequest<void>(`${API_URLS.EMAIL.ACCOUNTS}/${accountId}/emails/${emailId}`, {
      method: 'DELETE',
      params: { permanent },
    });
  },

  // 标记邮件已读/未读
  markEmailRead: (accountId: number, emailId: number, isRead: boolean = true) => {
    return apiRequest<API.Email>(`${API_URLS.EMAIL.ACCOUNTS}/${accountId}/emails/${emailId}/mark-read`, {
      method: 'POST',
      params: { is_read: isRead },
    });
  },

  // 标记邮件重要/取消重要
  markEmailFlagged: (accountId: number, emailId: number, isFlagged: boolean = true) => {
    return apiRequest<API.Email>(`${API_URLS.EMAIL.ACCOUNTS}/${accountId}/emails/${emailId}/mark-flagged`, {
      method: 'POST',
      params: { is_flagged: isFlagged },
    });
  },

  // 移动邮件到指定文件夹
  moveEmail: (accountId: number, emailId: number, folder: string) => {
    return apiRequest<API.Email>(`${API_URLS.EMAIL.ACCOUNTS}/${accountId}/emails/${emailId}/move`, {
      method: 'POST',
      params: { folder },
    });
  },
}; 