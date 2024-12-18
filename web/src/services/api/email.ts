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

export interface UpdateEmailAccountParams {
  email_address?: string;
  auth_token?: string;
  smtp_host?: string;
  smtp_port?: number;
  imap_host?: string;
  imap_port?: number;
  use_ssl?: boolean;
  use_tls?: boolean;
}

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

// 标签相关接口
export interface EmailTagAction {
  name: string;
  action_name: string;
  description: string;
}

export interface EmailTag {
  id: number;
  name: string;
  color: string;
  description?: string;
  action_name?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTagParams {
  name: string;
  color: string;
  description?: string;
  action_name?: string;
}

export interface UpdateTagParams {
  name?: string;
  color?: string;
  description?: string;
  action_name?: string;
}

export interface SendEmailParams {
  account_id: number;
  recipients: string;
  cc?: string;
  bcc?: string;
  subject: string;
  content: string;
  content_type?: string;
  attachments?: string;
  reply_to_email_id?: number;
  reply_type?: string;
}

declare namespace API {
  interface EmailPreReply {
    id: number;
    subject: string;
    recipients: string;
    cc?: string;
    bcc?: string;
    content: string;
    content_type: string;
    created_at: string;
    status: string;
  }
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

  // ���新邮件账户
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

  // 获取所有标签
  getTags: () => {
    return apiRequest<EmailTag[]>('/api/user/email/tags', {
      method: 'GET',
    });
  },

  // 创建标签
  createTag: (params: CreateTagParams) => {
    return apiRequest<EmailTag>('/api/user/email/tags', {
      method: 'POST',
      data: params,
    });
  },

  // 更新标签
  updateTag: (tagId: number, params: UpdateTagParams) => {
    return apiRequest<EmailTag>(`/api/user/email/tags/${tagId}`, {
      method: 'PUT',
      data: params,
    });
  },

  // 删除标签
  deleteTag: (tagId: number) => {
    return apiRequest<void>(`/api/user/email/tags/${tagId}`, {
      method: 'DELETE',
    });
  },

  // 为邮件添加标签
  addEmailTag: (emailId: number, tagId: number) => {
    return apiRequest<void>(`/api/user/email/emails/${emailId}/tags/${tagId}`, {
      method: 'POST',
    });
  },

  // 移除邮件标签
  removeEmailTag: (emailId: number, tagId: number) => {
    return apiRequest<void>(`/api/user/email/emails/${emailId}/tags/${tagId}`, {
      method: 'DELETE',
    });
  },

  // 获取标签动作列表
  getTagActions: () => {
    return apiRequest<EmailTagAction[]>('/api/user/email/tag/actions', {
      method: 'GET',
    });
  },

  // 预发送邮件
  sendEmail: (params: SendEmailParams) => {
    return apiRequest<void>('/api/user/email-outbox/send', {
      method: 'POST',
      data: params,
    });
  },

  // 直接发送邮件
  sendEmailDirect: (params: SendEmailParams) => {
    return apiRequest<void>('/api/user/email-outbox/send-direct', {
      method: 'POST',
      data: params,
    });
  },

  // 获取发件箱列表
  getOutboxList: (params?: {
    skip?: number;
    limit?: number;
    status?: string;
    reply_type?: string;
    account_id?: number;
    search?: string;
    start_date?: string;
    end_date?: string;
  }) => {
    return apiRequest<API.ListResponse<API.EmailOutbox>>('/api/user/email-outbox/list', {
      method: 'GET',
      params,
    });
  },

  // 获取发件箱邮件详情
  getOutboxEmail: (emailId: number) => {
    return apiRequest<API.EmailOutbox>(`/api/user/email-outbox/${emailId}`, {
      method: 'GET',
    });
  },

  // 删除发件箱邮件
  deleteOutboxEmail: (emailId: number) => {
    return apiRequest<void>(`/api/user/email-outbox/${emailId}`, {
      method: 'DELETE',
    });
  },

  // 重新发送失败的邮件
  resendEmail: (emailId: number) => {
    return apiRequest<API.EmailOutbox>(`/api/user/email-outbox/${emailId}/resend`, {
      method: 'POST',
    });
  },

  // 获取预回复内容
  getPreReply: (preReplyId: number) => {
    return apiRequest<API.EmailOutbox>(`/api/user/email-outbox/${preReplyId}`, {
      method: 'GET',
    });
  },

  // 更新预回复邮件
  updatePreReply: (id: number, params: SendEmailParams) => {
    return apiRequest<API.EmailOutbox>(`/api/user/email-outbox/pre-reply/${id}`, {
      method: 'PUT',
      data: params,
    });
  },

  // 发送预回复邮件
  sendPreReply: (id: number) => {
    return apiRequest<void>(`/api/user/email-outbox/${id}/send`, {
      method: 'POST',
    });
  },
}; 