interface EnvConfig {
  API_URL: string;
  API_PREFIX: string;
}

const config: EnvConfig = {
  API_URL: process.env.API_URL || 'http://localhost:8112',
  API_PREFIX: process.env.API_PREFIX || '/api',
};

export default config; 