// API 路径配置
export const API_URLS = {
  // 用户相关
  USER: {
    LOGIN: '/api/user/login',
    REGISTER: '/api/user/register',
    PROFILE: '/api/user/me',
    VERIFY_CODE: '/api/user/send-verification-code',
  },
} as const; 