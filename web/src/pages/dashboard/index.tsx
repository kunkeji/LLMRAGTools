import React, { useState, useRef, useEffect } from 'react';
import { Input, Button, Avatar, Spin, message } from 'antd';
import { SendOutlined, UserOutlined, RobotOutlined, MessageOutlined } from '@ant-design/icons';
import { LoadingOutlined } from '@ant-design/icons';
import styles from './index.less';

const { TextArea } = Input;

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: number;
}

const EmptyState: React.FC = () => {
  const [dots, setDots] = useState('');
  
  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? '' : prev + '.');
    }, 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={styles.emptyState}>
      <MessageOutlined className={styles.icon} />
      <div className={styles.title}>AI 助手已准备就绪{dots}</div>
      <div className={styles.subtitle}>让我们开始一段智能对话</div>
    </div>
  );
};

const DashboardPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textAreaRef = useRef<any>(null);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      const behavior = messages.length > 1 ? 'smooth' : 'auto';
      messagesEndRef.current.scrollIntoView({ behavior });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (textAreaRef.current) {
      textAreaRef.current.focus();
    }
  }, []);

  const handleSend = async () => {
    if (!inputValue.trim() || loading) {
      return;
    }

    const userMessage: ChatMessage = {
      role: 'user',
      content: inputValue.trim(),
      timestamp: Date.now(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:8112/api/user/feature-mappings/execute/CHAT', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({ message: userMessage.content }),
      });

      if (!response.ok) {
        throw new Error('聊天请求失败');
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法读取响应流');
      }

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: '',
        timestamp: Date.now(),
      };
      setMessages(prev => [...prev, assistantMessage]);

      const decoder = new TextDecoder();
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const text = decoder.decode(value);
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1].content += text;
          return newMessages;
        });
      }
    } catch (error: any) {
      message.error({
        content: error.message || '发送失败',
        className: styles.errorMessage,
      });
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
      setIsTyping(false);
      if (textAreaRef.current) {
        textAreaRef.current.focus();
      }
    }
  };

  const formatTime = (timestamp?: number) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={styles.container}>
      <div className={styles.chatContainer}>
        <div className={styles.messageList}>
          {messages.length === 0 && !isTyping && <EmptyState />}
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`${styles.messageWrapper} ${msg.role === 'user' ? styles.userMessage : styles.assistantMessage}`}
            >
              <div className={styles.messageContent}>
                <Avatar
                  icon={msg.role === 'user' ? <UserOutlined /> : <RobotOutlined />}
                  className={styles.avatar}
                  size={36}
                />
                <div className={styles.messageBody}>
                  <div className={styles.messageText}>
                    {msg.content}
                  </div>
                  <div className={styles.timestamp}>
                    {formatTime(msg.timestamp)}
                  </div>
                </div>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className={`${styles.messageWrapper} ${styles.assistantMessage}`}>
              <div className={styles.messageContent}>
                <Avatar
                  icon={<RobotOutlined />}
                  className={styles.avatar}
                  size={36}
                />
                <div className={styles.messageBody}>
                  <div className={styles.messageText}>
                    <Spin indicator={<LoadingOutlined style={{ fontSize: 24, color: 'rgba(255, 255, 255, 0.8)' }} spin />} />
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <div className={styles.inputWrapper}>
          <TextArea
            ref={textAreaRef}
            value={inputValue}
            onChange={e => setInputValue(e.target.value)}
            placeholder="输入消息，与 AI 助手对话..."
            autoSize={{ minRows: 1, maxRows: 4 }}
            onPressEnter={e => {
              if (!e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            disabled={loading}
            className={styles.textarea}
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={handleSend}
            loading={loading}
            className={styles.sendButton}
            disabled={!inputValue.trim() || loading}
          />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage; 