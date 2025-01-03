// API 路径配置
export const API_URLS = {
  // 用户相关
  USER: {
    LOGIN: '/api/user/login',
    REGISTER: '/api/user/register',
    PROFILE: '/api/user/me',
    VERIFY_CODE: '/api/user/send-verification-code',
    FORGOT_PASSWORD: '/api/user/password/forgot',
    RESET_PASSWORD: '/api/user/password/reset',
    UPDATE_PROFILE: '/api/user/profile/me',
    UPDATE_AVATAR: '/api/user/profile/me/avatar',
    // LLM 相关
    LLM_MODELS: '/api/user/llm/models',
    CHANNELS: '/api/user/channel',
    // 文档相关
    DOCUMENTS: '/api/user/documents',
  },
  // 邮件相关
  EMAIL: {
    ACCOUNTS: '/api/user/email/accounts',
    PROVIDERS: '/api/user/email/providers',
  },
} as const; 