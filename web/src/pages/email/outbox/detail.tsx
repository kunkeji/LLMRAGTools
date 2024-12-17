import React, { useState, useEffect } from 'react';
import { Card, Descriptions, Button, Space, message, Tag, Typography, Divider } from 'antd';
import { ArrowLeftOutlined, DeleteOutlined, RedoOutlined } from '@ant-design/icons';
import { useParams, history } from '@umijs/max';
import { emailApi } from '@/services/api/email';
import styles from './detail.less';

const { Title } = Typography;

const EmailOutboxDetail: React.FC = () => {
  const { emailId } = useParams<{ emailId: string }>();
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState<API.EmailOutbox>();

  // 加载邮件详情
  const loadEmail = async () => {
    if (!emailId) return;
    try {
      setLoading(true);
      const data = await emailApi.getOutboxEmail(parseInt(emailId));
      setEmail(data);
    } catch (error: any) {
      message.error(error.message || '加载邮件详情失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEmail();
  }, [emailId]);

  // 删除邮件
  const handleDelete = async () => {
    if (!emailId) return;
    try {
      await emailApi.deleteOutboxEmail(parseInt(emailId));
      message.success('删除成功');
      history.back();
    } catch (error: any) {
      message.error(error.message || '删除失败');
    }
  };

  // 重新发送
  const handleResend = async () => {
    if (!emailId) return;
    try {
      await emailApi.resendEmail(parseInt(emailId));
      message.success('已重新发送');
      loadEmail();
    } catch (error: any) {
      message.error(error.message || '重新发送失败');
    }
  };

  // 获取状态标签配置
  const getStatusConfig = (status: string) => {
    const config: Record<string, { color: string; text: string }> = {
      draft: { color: 'default', text: '草稿' },
      pending: { color: 'processing', text: '发送中' },
      sent: { color: 'success', text: '已发送' },
      failed: { color: 'error', text: '发送失败' },
    };
    return config[status] || { color: 'default', text: status };
  };

  // 获取回复类型显示文本
  const getReplyTypeText = (type?: string) => {
    const types: Record<string, string> = {
      pre_reply: '预设回复',
      auto_reply: '自动回复',
      manual_reply: '手动回复',
      quick_reply: '快速回复',
    };
    return type ? types[type] || type : '-';
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
                {email.status === 'failed' && (
                  <Button
                    type="primary"
                    icon={<RedoOutlined />}
                    onClick={handleResend}
                  >
                    重新发送
                  </Button>
                )}
                <Button
                  type="text"
                  danger
                  icon={<DeleteOutlined />}
                  onClick={handleDelete}
                >
                  删除
                </Button>
              </Space>
            </div>

            <Divider style={{ margin: '16px 0' }} />

            <Descriptions column={1}>
              <Descriptions.Item label="收件人">
                {email.recipients}
              </Descriptions.Item>
              {email.cc && (
                <Descriptions.Item label="抄送">
                  {email.cc}
                </Descriptions.Item>
              )}
              {email.bcc && (
                <Descriptions.Item label="密送">
                  {email.bcc}
                </Descriptions.Item>
              )}
              <Descriptions.Item label="状态">
                {(() => {
                  const config = getStatusConfig(email.status);
                  return <Tag color={config.color}>{config.text}</Tag>;
                })()}
              </Descriptions.Item>
              {email.reply_type && (
                <Descriptions.Item label="回复类型">
                  {getReplyTypeText(email.reply_type)}
                </Descriptions.Item>
              )}
              {email.send_time && (
                <Descriptions.Item label="发送时间">
                  {new Date(email.send_time).toLocaleString()}
                </Descriptions.Item>
              )}
              {email.error_message && (
                <Descriptions.Item label="错误信息">
                  <span style={{ color: '#ff4d4f' }}>{email.error_message}</span>
                </Descriptions.Item>
              )}
            </Descriptions>

            <Divider style={{ margin: '16px 0' }} />

            <div
              className={styles.content}
              dangerouslySetInnerHTML={{
                __html: email.content_type === 'text/html' ? email.content : email.content.replace(/\n/g, '<br/>'),
              }}
            />
          </>
        )}
      </Card>
    </div>
  );
};

export default EmailOutboxDetail; 