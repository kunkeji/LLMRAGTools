import React, { useState, useEffect } from 'react';
import { Card, Descriptions, Button, Space, message, Tag, Typography, Divider, Dropdown, Menu, Form, Table } from 'antd';
import { ArrowLeftOutlined, StarOutlined, StarFilled, DeleteOutlined, DownloadOutlined, TagOutlined } from '@ant-design/icons';
import { useParams, history } from '@umijs/max';
import { emailApi } from '@/services/api/email';
import type { EmailTag } from '@/services/api/email';
import styles from './detail.less';

const { Title } = Typography;

interface EmailReply {
  id: number;
  subject: string;
  status: string;
  created_at: string;
  send_time: string | null;
}

interface EmailResponse {
  id: number;
  subject: string;
  content: string;
  content_type: string;
  from_address: string;
  from_name: string | null;
  to_address: string[];
  cc_address: string[];
  bcc_address: string[];
  date: string;
  is_read: boolean;
  is_flagged: boolean;
  has_attachments: boolean;
  attachments: API.EmailAttachment[];
  tags: EmailTag[];
  replies: {
    pre_replies: EmailReply[];
    auto_replies: EmailReply[];
    manual_replies: EmailReply[];
    quick_replies: EmailReply[];
  };
}

const EmailDetail: React.FC = () => {
  const { accountId, emailId } = useParams<{ accountId: string; emailId: string }>();
  const [loading, setLoading] = useState(false);
  const [emailData, setEmailData] = useState<EmailResponse>();
  const [tags, setTags] = useState<EmailTag[]>([]);

  // 加载邮件详情和标签
  const loadData = async () => {
    if (!accountId || !emailId) return;
    try {
      setLoading(true);
      const [emailResponse, tagsData] = await Promise.all([
        emailApi.getEmail(parseInt(accountId), parseInt(emailId)),
        emailApi.getTags(),
      ]);
      setEmailData(emailResponse);
      setTags(tagsData);
      // 标记为已读
      if (!emailResponse.is_read) {
        await emailApi.markEmailRead(parseInt(accountId), parseInt(emailId), true);
      }
    } catch (error: any) {
      message.error(error.message || '加载邮件详情失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [accountId, emailId]);

  // 标记重要/取消重要
  const handleMarkFlagged = async (isFlagged: boolean) => {
    if (!accountId || !emailId || !emailData) return;
    try {
      await emailApi.markEmailFlagged(parseInt(accountId), parseInt(emailId), isFlagged);
      message.success(isFlagged ? '已标记为重要' : '已取消重要标记');
      loadData();
    } catch (error: any) {
      message.error(error.message || '操作失败');
    }
  };

  // 删除邮件
  const handleDelete = async () => {
    if (!accountId || !emailId) return;
    try {
      await emailApi.deleteEmail(parseInt(accountId), parseInt(emailId));
      message.success('删除成功');
      history.back();
    } catch (error: any) {
      message.error(error.message || '删除失败');
    }
  };

  // 处理标签
  const handleEmailTag = async (tagId: number, hasTag: boolean) => {
    if (!accountId || !emailId) return;
    try {
      if (hasTag) {
        await emailApi.removeEmailTag(parseInt(emailId), tagId);
        message.success('标签已移除');
      } else {
        await emailApi.addEmailTag(parseInt(emailId), tagId);
        message.success('标签已添加');
      }
      loadData();
    } catch (error: any) {
      message.error(error.message || '操作失败');
    }
  };

  // 标签菜单
  const tagMenu = (
    <Menu>
      {tags.map(tag => (
        <Menu.Item
          key={tag.id}
          onClick={() => handleEmailTag(tag.id, emailData?.tags?.some(t => t.id === tag.id) || false)}
        >
          <Space>
            <Tag color={tag.color}>{tag.name}</Tag>
            {emailData?.tags?.some(t => t.id === tag.id) && <span style={{ color: '#52c41a' }}>✓</span>}
          </Space>
        </Menu.Item>
      ))}
    </Menu>
  );

  // 下载附件
  const handleDownloadAttachment = (attachment: API.EmailAttachment) => {
    // TODO: 实现附件下载功能
    message.info('附件下载功能开发中');
  };

  // 回复列表列配置
  const replyColumns = [
    {
      title: '主题',
      dataIndex: 'subject',
      key: 'subject',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const statusConfig = {
          draft: { color: 'default', text: '草稿' },
          pending: { color: 'processing', text: '发送中' },
          sent: { color: 'success', text: '已发送' },
          failed: { color: 'error', text: '发送失败' },
        };
        const config = statusConfig[status as keyof typeof statusConfig] || { color: 'default', text: status };
        return <Tag color={config.color}>{config.text}</Tag>;
      },
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (time: string) => new Date(time).toLocaleString(),
    },
    {
      title: '发送时间',
      dataIndex: 'send_time',
      key: 'send_time',
      render: (time: string | null) => time ? new Date(time).toLocaleString() : '-',
    },
    {
      title: '操作',
      key: 'action',
      render: (record: EmailReply) => {
        // 如果是预回复并且状态不是send，跳转到编辑页面
        if (emailData?.replies.pre_replies.some(reply => reply.id === record.id && reply.status !== 'sent')) {
          return (
            <Button
              type="link"
              onClick={() => history.push(`/email/compose?account_id=${accountId}&pre_reply_id=${record.id}`)}
            >
              编辑
            </Button>
          );
        }
        // 其他类型的回复跳转到详情页面
        return (
          <Button
            type="link"
            onClick={() => history.push(`/email/outbox/${record.id}`)}
          >
            查看
          </Button>
        );
      },
    },
  ];

  return (
    <div className={styles.container}>
      <Card loading={loading}>
        {emailData && (
          <>
            <div className={styles.header}>
              <Space>
                <Button
                  type="link"
                  icon={<ArrowLeftOutlined />}
                  onClick={() => history.back()}
                >
                  返回
                </Button>
                <Title level={4}>{emailData.subject}</Title>
              </Space>
              <Space>
                <Button
                  type="primary"
                  onClick={() => history.push(`/email/compose?account_id=${accountId}&reply_to=${emailId}&reply_type=manual_reply`)}
                >
                  回复
                </Button>
                <Dropdown overlay={tagMenu} trigger={['click']}>
                  <Button
                    type="text"
                    icon={<TagOutlined />}
                  />
                </Dropdown>
                <Button
                  type="text"
                  icon={emailData.is_flagged ? <StarFilled style={{ color: '#faad14' }} /> : <StarOutlined />}
                  onClick={() => handleMarkFlagged(!emailData.is_flagged)}
                />
                <Button
                  type="text"
                  danger
                  icon={<DeleteOutlined />}
                  onClick={handleDelete}
                />
              </Space>
            </div>

            <Divider style={{ margin: '16px 0' }} />

            <Descriptions column={1}>
              <Descriptions.Item label="发件人">
                {emailData.from_name ? (
                  <>
                    <span>{emailData.from_name}</span>
                    <span style={{ marginLeft: 8, color: '#666' }}>
                      &lt;{emailData.from_address}&gt;
                    </span>
                  </>
                ) : (
                  emailData.from_address
                )}
              </Descriptions.Item>
              <Descriptions.Item label="收件人">
                {emailData.to_address.join(', ')}
              </Descriptions.Item>
              {emailData.cc_address.length > 0 && (
                <Descriptions.Item label="抄送">
                  {emailData.cc_address.join(', ')}
                </Descriptions.Item>
              )}
              <Descriptions.Item label="时间">
                {new Date(emailData.date).toLocaleString()}
              </Descriptions.Item>
              {emailData.tags && emailData.tags.length > 0 && (
                <Descriptions.Item label="标签">
                  <Space>
                    {emailData.tags.map(tag => (
                      <Tag
                        key={tag.id}
                        color={tag.color}
                        closable
                        onClose={(e) => {
                          e.preventDefault();
                          handleEmailTag(tag.id, true);
                        }}
                      >
                        {tag.name}
                      </Tag>
                    ))}
                  </Space>
                </Descriptions.Item>
              )}
            </Descriptions>

            {emailData.has_attachments && emailData.attachments.length > 0 && (
              <>
                <Divider style={{ margin: '16px 0' }} />
                <div className={styles.attachments}>
                  <div className={styles.attachmentsTitle}>附件：</div>
                  <Space wrap>
                    {emailData.attachments.map((attachment) => (
                      <Button
                        key={attachment.id}
                        icon={<DownloadOutlined />}
                        onClick={() => handleDownloadAttachment(attachment)}
                      >
                        {attachment.filename}
                        <span style={{ marginLeft: 8, fontSize: 12, color: '#666' }}>
                          ({Math.round(attachment.size / 1024)}KB)
                        </span>
                      </Button>
                    ))}
                  </Space>
                </div>
              </>
            )}

            <Divider style={{ margin: '16px 0' }} />

            <div
              className={styles.content}
              dangerouslySetInnerHTML={{
                __html: emailData.content_type === 'text/html' ? emailData.content : emailData.content.replace(/\n/g, '<br/>'),
              }}
            />

            {/* 预回复和已回复邮件列表 */}
            {(emailData.replies.pre_replies.length > 0 ||
              emailData.replies.auto_replies.length > 0 ||
              emailData.replies.manual_replies.length > 0 ||
              emailData.replies.quick_replies.length > 0) && (
              <>
                <Divider style={{ margin: '24px 0' }} />
                <div className={styles.replies}>
                  <Title level={5}>相关回复</Title>

                  {emailData.replies.pre_replies.length > 0 && (
                    <>
                      <div className={styles.replySection}>
                        <h4>预设回复</h4>
                        <Table
                          columns={replyColumns}
                          dataSource={emailData.replies.pre_replies}
                          rowKey="id"
                          size="small"
                          pagination={false}
                        />
                      </div>
                    </>
                  )}

                  {emailData.replies.auto_replies.length > 0 && (
                    <>
                      <div className={styles.replySection}>
                        <h4>自动回复</h4>
                        <Table
                          columns={replyColumns}
                          dataSource={emailData.replies.auto_replies}
                          rowKey="id"
                          size="small"
                          pagination={false}
                        />
                      </div>
                    </>
                  )}

                  {emailData.replies.manual_replies.length > 0 && (
                    <>
                      <div className={styles.replySection}>
                        <h4>手动回复</h4>
                        <Table
                          columns={replyColumns}
                          dataSource={emailData.replies.manual_replies}
                          rowKey="id"
                          size="small"
                          pagination={false}
                        />
                      </div>
                    </>
                  )}

                  {emailData.replies.quick_replies.length > 0 && (
                    <>
                      <div className={styles.replySection}>
                        <h4>快速回复</h4>
                        <Table
                          columns={replyColumns}
                          dataSource={emailData.replies.quick_replies}
                          rowKey="id"
                          size="small"
                          pagination={false}
                        />
                      </div>
                    </>
                  )}
                </div>
              </>
            )}

            <Divider style={{ margin: '24px 0' }} />

            <div className={styles.quickReply}>
              <Title level={5}>快速回复</Title>
              <Form
                onFinish={() => {
                  history.push(`/email/compose?account_id=${accountId}&reply_to=${emailId}&reply_type=quick_reply`);
                }}
              >
                <Form.Item>
                  <Button type="primary" htmlType="submit">
                    写回复
                  </Button>
                </Form.Item>
              </Form>
            </div>
          </>
        )}
      </Card>
    </div>
  );
};

export default EmailDetail; 