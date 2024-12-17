import React, { useState, useEffect } from 'react';
import { Card, Descriptions, Button, Space, message, Tag, Typography, Divider, Dropdown, Menu, Form } from 'antd';
import { ArrowLeftOutlined, StarOutlined, StarFilled, DeleteOutlined, DownloadOutlined, TagOutlined } from '@ant-design/icons';
import { useParams, history } from '@umijs/max';
import { emailApi } from '@/services/api/email';
import type { EmailTag } from '@/services/api/email';
import styles from './detail.less';

const { Title } = Typography;

const EmailDetail: React.FC = () => {
  const { accountId, emailId } = useParams<{ accountId: string; emailId: string }>();
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState<API.Email>();
  const [tags, setTags] = useState<EmailTag[]>([]);

  // 加载邮件详情和标签
  const loadData = async () => {
    if (!accountId || !emailId) return;
    try {
      setLoading(true);
      const [emailData, tagsData] = await Promise.all([
        emailApi.getEmail(parseInt(accountId), parseInt(emailId)),
        emailApi.getTags(),
      ]);
      setEmail(emailData);
      setTags(tagsData);
      // 标记为已读
      if (!emailData.is_read) {
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
    if (!accountId || !emailId) return;
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
      message.error(error.message || '��作失败');
    }
  };

  // 标签菜单
  const tagMenu = (
    <Menu>
      {tags.map(tag => (
        <Menu.Item
          key={tag.id}
          onClick={() => handleEmailTag(tag.id, email?.tags?.includes(tag.id) || false)}
        >
          <Space>
            <Tag color={tag.color}>{tag.name}</Tag>
            {email?.tags?.includes(tag.id) && <span style={{ color: '#52c41a' }}>✓</span>}
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

  return (
    <div className={styles.container}>
      <Card loading={loading}>
        {email && (
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
                <Title level={4}>{email.subject}</Title>
              </Space>
              <Space>
                <Button
                  type="primary"
                  onClick={() => history.push(`/email/compose?account_id=${accountId}&reply_to=${emailId}&reply_type=reply`)}
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
                  icon={email.is_flagged ? <StarFilled style={{ color: '#faad14' }} /> : <StarOutlined />}
                  onClick={() => handleMarkFlagged(!email.is_flagged)}
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
                {email.from_name ? (
                  <>
                    <span>{email.from_name}</span>
                    <span style={{ marginLeft: 8, color: '#666' }}>
                      &lt;{email.from_address}&gt;
                    </span>
                  </>
                ) : (
                  email.from_address
                )}
              </Descriptions.Item>
              <Descriptions.Item label="收件人">
                {email.to_address.join(', ')}
              </Descriptions.Item>
              {email.cc_address.length > 0 && (
                <Descriptions.Item label="抄送">
                  {email.cc_address.join(', ')}
                </Descriptions.Item>
              )}
              <Descriptions.Item label="时间">
                {new Date(email.date).toLocaleString()}
              </Descriptions.Item>
              {email.tags && email.tags.length > 0 && (
                <Descriptions.Item label="标签">
                  <Space>
                    {email.tags.map(tag => (
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

            {email.has_attachments && email.attachments.length > 0 && (
              <>
                <Divider style={{ margin: '16px 0' }} />
                <div className={styles.attachments}>
                  <div className={styles.attachmentsTitle}>附件：</div>
                  <Space wrap>
                    {email.attachments.map((attachment) => (
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
                __html: email.content_type === 'text/html' ? email.content : email.content.replace(/\n/g, '<br/>'),
              }}
            />

            <Divider style={{ margin: '24px 0' }} />

            <div className={styles.quickReply}>
              <Title level={5}>快速回复</Title>
              <Form
                onFinish={(values) => {
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