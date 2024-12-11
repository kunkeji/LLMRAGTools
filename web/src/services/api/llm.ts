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
}; 