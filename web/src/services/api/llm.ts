import { apiRequest } from './request';
import { API_URLS } from './config';

export interface CreateChannelParams {
  channel_name: string;
  model_type: string;
  model: string;
  api_key: string;
  proxy_url?: string;
}

export interface UpdateChannelParams extends Partial<CreateChannelParams> {}

// 功能映射相关接口
export interface Feature {
  feature_type: string;
  name: string;
  description: string;
  default_prompt: string;
}

export interface FeatureMapping {
  id: number;
  user_id: number;
  channel_id: number;
  feature_type: string;
  prompt_template?: string;
  last_used_at?: string;
  use_count: number;
  created_at: string;
  updated_at: string;
}

export interface SaveFeatureMappingParams {
  channel_id: number;
  feature_type: string;
  prompt_template?: string;
}

export const llmApi = {
  // 获取可用的 LLM 模型列表
  getModels: () => {
    return apiRequest<API.LLMModel[]>(API_URLS.USER.LLM_MODELS, {
      method: 'GET',
    });
  },

  // 获取渠道列表
  getChannels: (params?: API.PageParams) => {
    return apiRequest<API.LLMChannel[]>(API_URLS.USER.CHANNELS, {
      method: 'GET',
      params,
    });
  },

  // 获取渠道详情
  getChannel: (id: number) => {
    return apiRequest<API.LLMChannel>(`${API_URLS.USER.CHANNELS}/${id}`, {
      method: 'GET',
    });
  },

  // 创建渠道
  createChannel: (params: CreateChannelParams) => {
    return apiRequest<API.LLMChannel>(API_URLS.USER.CHANNELS, {
      method: 'POST',
      data: params,
    });
  },

  // 更新渠道
  updateChannel: (id: number, params: UpdateChannelParams) => {
    return apiRequest<API.LLMChannel>(`${API_URLS.USER.CHANNELS}/${id}`, {
      method: 'PUT',
      data: params,
    });
  },

  // 删除渠道
  deleteChannel: (id: number) => {
    return apiRequest<void>(`${API_URLS.USER.CHANNELS}/${id}`, {
      method: 'DELETE',
    });
  },

  // 测试渠道
  testChannel: (id: number) => {
    return apiRequest<void>(`${API_URLS.USER.CHANNELS}/${id}/test`, {
      method: 'POST',
    });
  },

  // 获取功能列表
  getFeatures: () => {
    return apiRequest<Feature[]>('/api/user/feature-mappings/features', {
      method: 'GET',
    });
  },

  // 获取用户功能映射
  getFeatureMappings: () => {
    return apiRequest<FeatureMapping[]>('/api/user/feature-mappings/mappings', {
      method: 'GET',
    });
  },

  // 保存功能映射
  saveFeatureMapping: (params: SaveFeatureMappingParams) => {
    return apiRequest<FeatureMapping>('/api/user/feature-mappings/mappings/save', {
      method: 'POST',
      data: params,
    });
  },
}; 