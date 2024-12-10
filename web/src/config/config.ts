interface EnvConfig {
  API_URL: string;
  API_PREFIX: string;
}

const config: EnvConfig = {
  API_URL: process.env.API_URL || 'http://127.0.0.1:8112',
  API_PREFIX: process.env.API_PREFIX || '/api',
};

// 导出完整的 API URL
export const getApiUrl = (path: string) => {
  if (path.startsWith('http')) {
    return path;
  }
  return `${config.API_URL}${path}`;
};

export default config; 