declare namespace API {
  interface Response<T = any> {
    code: string;
    data: T;
    message: string;
  }

  interface CurrentUser {
    id: number;
    username: string;
    email: string;
    nickname?: string;
    phone_number?: string;
    avatar?: string;
    status: 'active' | 'inactive';
    created_at: string;
    updated_at: string;
  }

  interface LoginResult {
    access_token: string;
    token_type: string;
  }

  interface PageParams {
    current?: number;
    pageSize?: number;
  }

  interface PageResult<T> {
    list: T[];
    total: number;
    page: number;
    pageSize: number;
  }

  interface ProxyStats {
    total: number;
    online: number;
    offline: number;
    uptime: string;
  }

  // 后端返回的原始流量数据格式
  interface RawProxyTraffic {
    timestamp: string;
    inbound: number;
    outbound: number;
  }

  // 图表使用的流量数据格式
  interface ProxyTraffic {
    timestamp: string;
    type: 'inbound' | 'outbound';
    value: number;
  }

  interface ProxyLog {
    id: number;
    proxy_id: number;
    proxy_name: string;
    event: string;
    details: string;
    timestamp: string;
  }

  // LLM 模型类型
  interface LLMModel {
    id: number;
    name: string;
    mapping_name: string;
    description: string;
  }


  // LLM 渠道类型
  interface LLMChannel {
    id: number;
    user_id: number;
    channel_name: string;
    model_type: string;
    model: string;
    api_key: string;
    proxy_url?: string;
    created_at: string;
    updated_at: string;
  }

  // 分页参数
  interface PageParams {
    skip?: number;
    limit?: number;
    keyword?: string;
    model_type?: string;
  }
}