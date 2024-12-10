import { request } from 'umi';

export interface LoginParams {
  username: string;
  password: string;
}

export interface RegisterParams {
  username: string;
  email: string;
  password: string;
}

export interface ChangePasswordParams {
  oldPassword: string;
  newPassword: string;
}

export async function login(params: LoginParams) {
  const formData = new FormData();
  formData.append('username', params.username);
  formData.append('password', params.password);

  return request<API.Response<API.LoginResult>>('/api/user/login', {
    method: 'POST',
    data: formData,
    requestType: 'form',
  });
}

export async function register(params: RegisterParams) {
  return request<API.Response<API.CurrentUser>>('/api/user/register', {
    method: 'POST',
    data: params,
  });
}

export async function logout() {
  return request<API.Response<void>>('/api/user/logout', {
    method: 'POST',
  });
}

export async function getCurrentUser() {
  return request<API.Response<API.CurrentUser>>('/api/user/me', {
    method: 'GET',
  });
}

export async function changePassword(params: ChangePasswordParams) {
  return request<API.Response<void>>('/api/user/change-password', {
    method: 'POST',
    data: params,
  });
}

export async function resetPassword(params: { email: string }) {
  return request<API.Response<void>>('/api/user/reset-password', {
    method: 'POST',
    data: params,
  });
} 