import { apiRequest } from './request';
import { API_URLS } from './config';

// 文档创建参数
export interface DocumentCreateParams {
  title: string;
  content: string;
  doc_type?: string;
  parent_id?: number;
  sort_order?: number;
}

// 文档更新参数
export interface DocumentUpdateParams {
  title?: string;
  content?: string;
  doc_type?: string;
  sort_order?: number;
}

// 文档移动参数
export interface DocumentMoveParams {
  parent_id?: number;
  sort_order?: number;
}

// 文档搜索参数
export interface DocumentSearchParams {
  keyword?: string;
  doc_type?: string;
  level?: number;
  parent_id?: number;
  skip?: number;
  limit?: number;
}

export const documentApi = {
  // 创建文档
  createDocument: (params: DocumentCreateParams) => {
    return apiRequest<API.Document>(`${API_URLS.USER.DOCUMENTS}`, {
      method: 'POST',
      data: params,
    });
  },

  // 获取文档树
  getDocumentTree: () => {
    return apiRequest<API.DocumentTreeNode[]>(`${API_URLS.USER.DOCUMENTS}/tree`, {
      method: 'GET',
    });
  },

  // 获取文档详情
  getDocument: (id: number) => {
    return apiRequest<API.Document>(`${API_URLS.USER.DOCUMENTS}/${id}`, {
      method: 'GET',
    });
  },

  // 更新文档
  updateDocument: (id: number, params: DocumentUpdateParams) => {
    return apiRequest<API.Document>(`${API_URLS.USER.DOCUMENTS}/${id}`, {
      method: 'PUT',
      data: params,
    });
  },

  // 移动文档
  moveDocument: (id: number, params: DocumentMoveParams) => {
    return apiRequest<API.Document>(`${API_URLS.USER.DOCUMENTS}/${id}/move`, {
      method: 'POST',
      data: params,
    });
  },

  // 删除文档
  deleteDocument: (id: number) => {
    return apiRequest<void>(`${API_URLS.USER.DOCUMENTS}/${id}`, {
      method: 'DELETE',
    });
  },

  // 搜索文档
  searchDocuments: (params: DocumentSearchParams) => {
    return apiRequest<API.Document[]>(`${API_URLS.USER.DOCUMENTS}`, {
      method: 'GET',
      params,
    });
  },
}; 