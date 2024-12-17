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
    deleted_at?: string;
    avg_response_time?: number;
    min_response_time?: number;
    max_response_time?: number;
    last_response_time?: number;
    last_test_time?: string;
    test_count?: number;
  }

  // 分页参数
  interface PageParams {
    skip?: number;
    limit?: number;
    keyword?: string;
    model_type?: string;
  }

  // 邮件同步状态
  type EmailSyncStatus = 'NEVER' | 'SYNCING' | 'SUCCESS' | 'ERROR';

  // 邮件账户类型
  interface EmailAccount {
    id: number;
    email_address: string;
    auth_token: string;
    smtp_host: string;
    smtp_port: number;
    imap_host: string;
    imap_port: number;
    use_ssl: boolean;
    use_tls: boolean;
    sync_status: EmailSyncStatus;
    last_sync_time?: string;
    smtp_last_test_time?: string;
    smtp_test_result?: boolean;
    smtp_test_error?: string;
    imap_last_test_time?: string;
    imap_test_result?: boolean;
    imap_test_error?: string;
    created_at: string;
    updated_at: string;
    user_id: number;
    provider?: string;
  }

  // 邮件服务商类型
  interface EmailProvider {
    id: number;
    name: string;
    domain_suffix: string;
    smtp_host: string;
    smtp_port: number;
    imap_host: string;
    imap_port: number;
    use_ssl: boolean;
    use_tls: boolean;
    is_active: boolean;
    logo_url: string | null;
    description: string;
    help_url: string | null;
    auth_help_url: string | null;
    sort_order: number;
    created_at: string;
    updated_at: string;
    deleted_at: string | null;
  }

  // 文档类型
  interface Document {
    id: number;
    title: string;
    content: string;
    doc_type?: string;
    parent_id?: number;
    path: string;
    order: number;
    creator_id: number;
    editor_id?: number;
    created_at: string;
    updated_at: string;
    deleted_at?: string;
  }

  // 文档树节点
  interface DocumentTreeNode {
    id: number;
    title: string;
    doc_type?: string;
    level: number;
    sort_order: number;
    has_children: boolean;
    children: DocumentTreeNode[];
  }

  // 文档树
  interface DocumentTree {
    nodes: DocumentTreeNode[];
    total: number;
  }

  // 邮件类型
  interface Email {
    id: number;
    account_id: number;
    message_id: string;
    subject: string;
    from_address: string;
    from_name: string | null;
    to_address: string[];
    cc_address: string[];
    bcc_address: string[];
    date: string;
    content_type: string;
    content: string;
    raw_content: string | null;
    has_attachments: boolean;
    size: number;
    is_read: boolean;
    is_flagged: boolean;
    is_deleted: boolean;
    folder: string;
    importance: number;
    in_reply_to: string | null;
    references: string[] | null;
    deleted_at: string | null;
    created_at: string;
    updated_at: string;
    attachments: EmailAttachment[];
    tags?: number[];
  }

  // 邮件附件类型
  interface EmailAttachment {
    id: number;
    email_id: number;
    filename: string;
    content_type: string;
    size: number;
    created_at: string;
    updated_at: string;
  }

  // 发件箱邮件类型
  interface EmailOutbox {
    id: number;
    status: 'draft' | 'pending' | 'sent' | 'failed';
    account_id: number;
    reply_to_email_id?: number;
    reply_type?: 'pre_reply' | 'auto_reply' | 'manual_reply' | 'quick_reply';
    recipients: string;
    cc?: string;
    bcc?: string;
    subject: string;
    content: string;
    content_type: string;
    attachments?: string;
    send_time?: string;
    error_message?: string;
    created_at: string;
    updated_at: string;
  }

  // 发件箱列表响应
  interface ListResponse<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
  }
}