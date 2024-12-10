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
}