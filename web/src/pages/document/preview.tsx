import React, { useState, useEffect } from 'react';
import { Card, Spin, message, Button, Space } from 'antd';
import { useParams, history } from '@umijs/max';
import { documentApi } from '@/services/api/document';
import { ArrowLeftOutlined, DownloadOutlined, FileWordOutlined } from '@ant-design/icons';
import { Document as DocxDocument, Packer, Paragraph, TextRun, HeadingLevel } from 'docx';
import { saveAs } from 'file-saver';
import '@wangeditor/editor/dist/css/style.css';
import styles from './preview.less';

const PreviewPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [loading, setLoading] = useState(false);
  const [docData, setDocData] = useState<API.Document>();

  useEffect(() => {
    const loadDocument = async () => {
      if (!id) return;
      try {
        setLoading(true);
        const data = await documentApi.getDocument(parseInt(id));
        setDocData(data);
      } catch (error: any) {
        message.error(error.message || '加载文档失败');
      } finally {
        setLoading(false);
      }
    };

    loadDocument();
  }, [id]);

  // 导出 HTML
  const handleExportHtml = () => {
    if (!docData) return;

    // 添加基本样式
    const style = window.document.createElement('style');
    style.textContent = `
      body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
      }
      h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a;
        margin-top: 24px;
        margin-bottom: 16px;
      }
      p {
        margin-bottom: 16px;
      }
      img {
        max-width: 100%;
        height: auto;
      }
      pre {
        background-color: #f6f6f6;
        padding: 16px;
        border-radius: 4px;
        overflow-x: auto;
      }
      code {
        font-family: Consolas, monospace;
      }
      blockquote {
        border-left: 4px solid #1890ff;
        padding-left: 16px;
        margin: 16px 0;
        color: #666;
      }
    `;

    // 创建完整的 HTML 文档
    const html = `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8">
          <title>${docData.title}</title>
          ${style.outerHTML}
        </head>
        <body>
          <h1>${docData.title}</h1>
          ${docData.content}
        </body>
      </html>
    `;

    // 创建 Blob 对象
    const blob = new Blob([html], { type: 'text/html' });
    
    // 创建下载链接
    const url = URL.createObjectURL(blob);
    const link = window.document.createElement('a');
    link.href = url;
    link.download = `${docData.title}.html`;
    
    // 触发下载
    window.document.body.appendChild(link);
    link.click();
    
    // 清理
    window.document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // 导出 Word
  const handleExportWord = async () => {
    if (!docData) return;

    try {
      // 创建一个临时的 div 来解析 HTML 内容
      const tempDiv = window.document.createElement('div');
      tempDiv.innerHTML = docData.content;

      // 将 HTML 内容转换为 docx 格式
      const docx = new DocxDocument({
        sections: [{
          properties: {},
          children: [
            new Paragraph({
              text: docData.title,
              heading: HeadingLevel.TITLE,
              spacing: {
                after: 200,
              },
            }),
            ...Array.from(tempDiv.children).map(child => {
              // 处理不同类型的内容
              if (child.tagName === 'H1') {
                return new Paragraph({
                  text: child.textContent || '',
                  heading: HeadingLevel.HEADING_1,
                  spacing: { before: 240, after: 120 },
                });
              } else if (child.tagName === 'H2') {
                return new Paragraph({
                  text: child.textContent || '',
                  heading: HeadingLevel.HEADING_2,
                  spacing: { before: 240, after: 120 },
                });
              } else if (child.tagName === 'H3') {
                return new Paragraph({
                  text: child.textContent || '',
                  heading: HeadingLevel.HEADING_3,
                  spacing: { before: 240, after: 120 },
                });
              } else if (child.tagName === 'BLOCKQUOTE') {
                return new Paragraph({
                  children: [
                    new TextRun({
                      text: child.textContent || '',
                      italics: true,
                    }),
                  ],
                  spacing: { before: 120, after: 120 },
                  indent: { left: 720 },
                });
              } else if (child.tagName === 'PRE') {
                return new Paragraph({
                  children: [
                    new TextRun({
                      text: child.textContent || '',
                      font: 'Consolas',
                    }),
                  ],
                  spacing: { before: 120, after: 120 },
                });
              } else {
                return new Paragraph({
                  text: child.textContent || '',
                  spacing: { before: 120, after: 120 },
                });
              }
            }),
          ],
        }],
      });

      // 生成 docx 文件
      const buffer = await Packer.toBlob(docx);
      saveAs(buffer, `${docData.title}.docx`);
      message.success('导出成功');
    } catch (error) {
      console.error('导出失败:', error);
      message.error('导出失败');
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <Card>
          <div style={{ textAlign: 'center', padding: '50px 0' }}>
            <Spin />
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Card>
        <div className={styles.document}>
          <div className={styles.documentHeader}>
            <Button
              type="link"
              icon={<ArrowLeftOutlined />}
              onClick={() => history.back()}
              className={styles.backButton}
            >
              返回编辑
            </Button>
            <h1>{docData?.title}</h1>
            <div className={styles.actions}>
              <Space>
                <Button
                  type="primary"
                  icon={<FileWordOutlined />}
                  onClick={handleExportWord}
                >
                  导出Word
                </Button>
              </Space>
            </div>
          </div>
          <div className={styles.documentContent}>
            <div
              className={styles.content}
              dangerouslySetInnerHTML={{ __html: docData?.content || '' }}
            />
          </div>
        </div>
      </Card>
    </div>
  );
};

export default PreviewPage; 