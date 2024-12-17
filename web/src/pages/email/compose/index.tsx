import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, Space, message, Select } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { history, useLocation } from '@umijs/max';
import { Editor, Toolbar } from '@wangeditor/editor-for-react';
import { IDomEditor, IEditorConfig, IToolbarConfig } from '@wangeditor/editor';
import { emailApi } from '@/services/api/email';
import '@wangeditor/editor/dist/css/style.css';
import styles from './index.less';
import { CUSTOM_BUTTON_KEY } from '../components/CustomButton';

const { Option } = Select;

const EmailCompose: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [accounts, setAccounts] = useState<API.EmailAccount[]>([]);
  const [editor, setEditor] = useState<IDomEditor | null>(null);
  const [html, setHtml] = useState('');
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const accountId = searchParams.get('account_id');
  const replyToEmailId = searchParams.get('reply_to');
  const replyType = searchParams.get('reply_type') || undefined;

  // 工具栏配置
  const toolbarConfig: Partial<IToolbarConfig> = {
    toolbarKeys: [
      'headerSelect',
      'bold',
      'italic',
      'underline',
      'through',
      'color',
      'bgColor',
      'lineHeight',
      '|',
      'bulletedList',
      'numberedList',
      'todo',
      '|',
      'insertLink',
      'insertTable',
      'codeBlock',
      'emotion',
      '|',
      'undo',
      'redo',
      "|",
      CUSTOM_BUTTON_KEY,
    ],
  };

  // 编辑器配置
  const editorConfig: Partial<IEditorConfig> = {
    placeholder: '请输入邮件内容...',
    autoFocus: false,
  };

  // 加载邮件账户列表
  useEffect(() => {
    const loadAccounts = async () => {
      try {
        const data = await emailApi.getAccounts();
        setAccounts(data);
        
        // 如果URL中有account_id,设置为默认值
        if (accountId) {
          form.setFieldValue('account_id', parseInt(accountId));
        }
      } catch (error: any) {
        message.error(error.message || '加载邮件账户失败');
      }
    };
    loadAccounts();
  }, []);

  // 如果是回复邮件,加载原始邮件信息
  useEffect(() => {
    const loadReplyEmail = async () => {
      if (!replyToEmailId || !accountId) return;
      try {
        const email = await emailApi.getEmail(parseInt(accountId), parseInt(replyToEmailId));
        
        // 设置收件人���主题
        form.setFieldsValue({
          recipients: email.from_address,
          subject: `Re: ${email.subject}`,
        });

        // 设置回复内容模板
        const replyTemplate = `
          <br/>
          <br/>
          <blockquote style="padding-left: 1em; border-left: 4px solid #ddd; margin: 0;">
            <p>在 ${new Date(email.date).toLocaleString()}，${email.from_name || email.from_address} 写道：</p>
            ${email.content}
          </blockquote>
        `;
        setHtml(replyTemplate);
      } catch (error: any) {
        message.error(error.message || '加载原始邮件失败');
      }
    };
    loadReplyEmail();
  }, [replyToEmailId, accountId]);

  // 处理发送邮件
  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      await emailApi.sendEmailDirect({
        ...values,
        content: html,
        content_type: 'text/html',
        reply_to_email_id: replyToEmailId ? parseInt(replyToEmailId) : undefined,
        reply_type: replyType,
      });
      message.success('邮件发送成功');
      history.back();
    } catch (error: any) {
      message.error(error.message || '发送失败');
    } finally {
      setLoading(false);
    }
  };

  // 监听编辑器内容变化
  const handleEditorChange = (editor: IDomEditor) => {
    setHtml(editor.getHtml());
  };

  // 组件销毁时销毁编辑器
  useEffect(() => {
    return () => {
      if (editor) {
        editor.destroy();
        setEditor(null);
      }
    };
  }, [editor]);

  return (
    <div className={styles.container}>
      <Card>
        <div className={styles.header}>
          <Space>
            <Button
              type="link"
              icon={<ArrowLeftOutlined />}
              onClick={() => history.back()}
            >
              返回
            </Button>
            <h2 className={styles.title}>写邮件</h2>
          </Space>
        </div>

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="account_id"
            label="发件账户"
            rules={[{ required: true, message: '请选择发件账户' }]}
          >
            <Select placeholder="请选择发件账户">
              {accounts.map(account => (
                <Option key={account.id} value={account.id}>
                  {account.email_address}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="recipients"
            label="收件人"
            rules={[{ required: true, message: '请输入收件人邮箱' }]}
            tooltip="多个邮箱请用分号(;)分隔"
          >
            <Input placeholder="请输入收件人邮箱,多个邮箱用分号(;)分隔" />
          </Form.Item>

          <Form.Item
            name="cc"
            label="抄送"
            tooltip="多个邮箱请用分号(;)分隔"
          >
            <Input placeholder="请输入抄送邮箱,多个邮箱用分号(;)分隔" />
          </Form.Item>

          <Form.Item
            name="bcc"
            label="密送"
            tooltip="多个邮箱请用分号(;)分隔"
          >
            <Input placeholder="请输入密送邮箱,多个邮箱用分号(;)分隔" />
          </Form.Item>

          <Form.Item
            name="subject"
            label="主题"
            rules={[{ required: true, message: '请输入邮件主题' }]}
          >
            <Input placeholder="请输入邮件主题" />
          </Form.Item>

          <Form.Item
            label="正文"
            required
          >
            <div className={styles.editor}>
              <Toolbar
                editor={editor}
                defaultConfig={toolbarConfig}
                mode="default"
                className={styles.toolbar}
              />
              <Editor
                defaultConfig={editorConfig}
                value={html}
                onCreated={setEditor}
                onChange={handleEditorChange}
                mode="default"
                className={styles.editorBody}
              />
            </div>
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={loading}>
                发送
              </Button>
              <Button onClick={() => history.back()}>取消</Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default EmailCompose; 