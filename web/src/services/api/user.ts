import { apiRequest } from './request';
import { API_URLS } from './config';

export interface LoginParams {
  username: string;
  password: string;
}

export interface RegisterParams {
  email: string;
  username: string;
  password: string;
  verification_code: string;
}

export interface SendVerificationCodeParams {
  email: string;
  purpose?: 'register' | 'reset_password';
}

export interface ResetPasswordParams {
  email: string;
  verification_code: string;
  new_password: string;
}

export const userApi = {
  // 登录
  login: (params: LoginParams) => {
    return apiRequest<API.LoginResult>(API_URLS.USER.LOGIN, {
      method: 'POST',
      data: params,
      requestType: 'form',
    });
  },

  // 注册
  register: (params: RegisterParams) => {
    return apiRequest<API.CurrentUser>(API_URLS.USER.REGISTER, {
      method: 'POST',
      data: params,
    });
  },

  // 获取当前用户信息
  getCurrentUser: () => {
    return apiRequest<API.CurrentUser>(API_URLS.USER.PROFILE, {
      method: 'GET',
    });
  },

  // 发送验证码
  sendVerificationCode: (params: SendVerificationCodeParams) => {
    return apiRequest<void>(API_URLS.USER.VERIFY_CODE, {
      method: 'POST',
      data: params,
    });
  },

  // 发送重置密码验证码
  sendResetPasswordCode: (email: string) => {
    return apiRequest<void>(API_URLS.USER.FORGOT_PASSWORD, {
      method: 'POST',
      data: email,
    });
  },

  // 重置密码
  resetPassword: (params: ResetPasswordParams) => {
    return apiRequest<void>(API_URLS.USER.RESET_PASSWORD, {
      method: 'POST',
      data: params,
    });
  },
}; 