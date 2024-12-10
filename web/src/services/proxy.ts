import { request } from 'umi';

export interface ProxyItem {
  id: number;
  name: string;
  host: string;
  port: number;
  status: 'online' | 'offline';
  protocol: string;
  created_at: string;
  updated_at: string;
}

export async function getProxyStats() {
  return request<API.Response<API.ProxyStats>>('/api/proxies/stats');
}

export async function getProxyList(params?: {
  page?: number;
  pageSize?: number;
  status?: string;
}) {
  return request<API.Response<API.PageResult<ProxyItem>>>('/api/proxies', {
    params,
  });
}

export async function getProxyTraffic(id: number, period: string = '24h') {
  return request<API.Response<API.RawProxyTraffic[]>>(`/api/proxies/${id}/traffic`, {
    params: { period },
  });
}

export async function createProxy(data: Partial<ProxyItem>) {
  return request<API.Response<ProxyItem>>('/api/proxies', {
    method: 'POST',
    data,
  });
}

export async function updateProxy(id: number, data: Partial<ProxyItem>) {
  return request<API.Response<ProxyItem>>(`/api/proxies/${id}`, {
    method: 'PUT',
    data,
  });
}

export async function deleteProxy(id: number) {
  return request<API.Response<void>>(`/api/proxies/${id}`, {
    method: 'DELETE',
  });
}

export async function getProxyLogs(id: number, params?: {
  page?: number;
  pageSize?: number;
  startTime?: string;
  endTime?: string;
}) {
  return request<API.Response<API.PageResult<API.ProxyLog>>>(`/api/proxies/${id}/logs`, {
    params,
  });
} 