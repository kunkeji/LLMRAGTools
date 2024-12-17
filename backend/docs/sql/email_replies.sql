-- 创建邮件发送表
CREATE TABLE IF NOT EXISTS email_outbox (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '发送ID',
    account_id INT NOT NULL COMMENT '发送邮箱账户ID',
    reply_to_email_id INT COMMENT '回复的原始邮件ID,为空表示新发送邮件',
    reply_type ENUM('pre_reply', 'auto_reply', 'manual_reply') COMMENT '回复类型,仅在回复邮件时使用',
    
    recipients TEXT NOT NULL COMMENT '收件人列表,多个邮箱用分号分隔',
    cc TEXT COMMENT '抄送列表,多个邮箱用分号分隔',
    bcc TEXT COMMENT '密送列表,多个邮箱用分号分隔',
    subject VARCHAR(500) COMMENT '邮件主题',
    content TEXT NOT NULL COMMENT '邮件内容',
    content_type VARCHAR(50) NOT NULL DEFAULT 'text/html' COMMENT '内容类型',
    
    attachments TEXT COMMENT '附件列表,JSON格式存储文件信息',
    status ENUM('draft', 'pending', 'sent', 'failed') NOT NULL DEFAULT 'draft' COMMENT '状态：draft=草稿,pending=待发送,sent=已发送,failed=发送失败',
    send_time DATETIME COMMENT '发送时间',
    error_message VARCHAR(500) COMMENT '错误信息',
    
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at TIMESTAMP NULL COMMENT '删除时间',
    
    FOREIGN KEY (account_id) REFERENCES email_accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (reply_to_email_id) REFERENCES emails(id) ON DELETE SET NULL,
    
    INDEX idx_account_id (account_id),
    INDEX idx_reply_to_email_id (reply_to_email_id),
    INDEX idx_reply_type (reply_type),
    INDEX idx_status (status),
    INDEX idx_send_time (send_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮件发送表'; 