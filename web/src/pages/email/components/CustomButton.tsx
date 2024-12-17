import { IDomEditor } from '@wangeditor/editor';
import { message } from 'antd';
import { Boot } from '@wangeditor/editor';
import { marked } from 'marked';

// AI帮写接口
async function* fetchAIWriting(message: string) {
  const response = await fetch('http://localhost:8112/api/user/feature-mappings/execute/EMAIL_REPLY', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    },
    body: JSON.stringify({ message }),
  });
  if (!response.ok) {
    throw new Error('AI写信请求失败');
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error('无法读取响应流');
  }

  const decoder = new TextDecoder();
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    const text = decoder.decode(value);
    yield text;
  }
}

// 自定义菜单类
class CustomButtonMenu {
  readonly title: string;
  readonly tag: string;

  constructor() {
    this.title = 'AI邮件';
    this.tag = 'button';
  }

  getValue(): string | boolean {
    return '';
  }

  isActive(): boolean {
    return false;
  }

  isDisabled(): boolean {
    return false;
  }

  async exec(editor: IDomEditor) {
    try {
      // 禁用编辑器
      editor.enable(false);

      // 获取选中的内容
      const selectedText = editor.getSelectionText() || '';

      // 构建消息
      const prompt = `要求：${selectedText}`;

      // 流式获取AI生成的内容
      let content = '';
      let messageall = '';
      for await (const chunk of fetchAIWriting(prompt)) {
        // 清空
        messageall += chunk;
        content = chunk;
        const html = `${content}`;
        editor.dangerouslyInsertHtml(html);
      }
      // AI 输出完成后，将 markdown 转换为 HTML
      const htmlContent = marked(messageall, {
        breaks: true,
        gfm: true,
      });

      // 替换为转换后的 HTML
      editor.setHtml(htmlContent);

      message.success('AI写作完成');
    } catch (error: any) {
      console.error('AI写作错误:', error);
      message.error(error.message || 'AI写作失败');
    } finally {
      // 重新启用编辑器
      editor.enable(true);
    }
  }
}

// 注册自定义菜单
Boot.registerMenu({
  key: 'customButton',
  factory() {
    return new CustomButtonMenu();
  },
});

export const CUSTOM_BUTTON_KEY = 'customButton';