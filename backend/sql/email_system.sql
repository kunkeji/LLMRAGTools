SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for emails
-- ----------------------------
DROP TABLE IF EXISTS `emails`;
CREATE TABLE `emails` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `account_id` int NOT NULL COMMENT '邮箱账户ID',
  `message_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮件唯一ID',
  `subject` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮件主题',
  `from_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发件人地址',
  `from_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发件人名称',
  `to_address` json NOT NULL COMMENT '收件人地址列表',
  `cc_address` json DEFAULT NULL COMMENT '抄送地址列表',
  `bcc_address` json DEFAULT NULL COMMENT '密送地址列表',
  `reply_to` json DEFAULT NULL COMMENT '回复地址列表',
  `date` datetime NOT NULL COMMENT '邮件发送时间',
  `content_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '内容类型(text/plain, text/html)',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '邮件内容',
  `raw_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '原始邮件内容',
  `has_attachments` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否有附件',
  `size` int NOT NULL DEFAULT '0' COMMENT '邮件大小(字节)',
  `is_read` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已读',
  `is_flagged` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否标记',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  `folder` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'INBOX' COMMENT '所在文件夹',
  `importance` tinyint NOT NULL DEFAULT '0' COMMENT '重要性(0-普通,1-重要,2-紧急)',
  `in_reply_to` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '回复的邮件ID',
  `references` json DEFAULT NULL COMMENT '相关邮件ID列表',
  `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_account_message_id` (`account_id`,`message_id`),
  KEY `idx_account_id` (`account_id`),
  KEY `idx_message_id` (`message_id`),
  KEY `idx_date` (`date`),
  KEY `idx_is_read` (`is_read`),
  KEY `idx_is_flagged` (`is_flagged`),
  KEY `idx_is_deleted` (`is_deleted`),
  KEY `idx_folder` (`folder`),
  KEY `idx_importance` (`importance`),
  CONSTRAINT `fk_emails_account_id` FOREIGN KEY (`account_id`) REFERENCES `email_accounts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮件表';

-- ----------------------------
-- Table structure for email_attachments
-- ----------------------------
DROP TABLE IF EXISTS `email_attachments`;
CREATE TABLE `email_attachments` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `email_id` int NOT NULL COMMENT '邮件ID',
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件名',
  `content_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件类型',
  `size` int NOT NULL COMMENT '文件大小(字节)',
  `storage_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '存储路径',
  `content_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '内联附件ID',
  `is_inline` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否内联附件',
  `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  KEY `idx_email_id` (`email_id`),
  CONSTRAINT `fk_attachments_email_id` FOREIGN KEY (`email_id`) REFERENCES `emails` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮件附件表';

-- ----------------------------
-- Table structure for email_sync_logs
-- ----------------------------
DROP TABLE IF EXISTS `email_sync_logs`;
CREATE TABLE `email_sync_logs` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `account_id` int NOT NULL COMMENT '邮箱账户ID',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `status` enum('RUNNING','COMPLETED','FAILED','CANCELLED','TIMEOUT') NOT NULL COMMENT '同步状态',
  `total_emails` int NOT NULL DEFAULT '0' COMMENT '同步邮件总数',
  `new_emails` int NOT NULL DEFAULT '0' COMMENT '新邮件数',
  `updated_emails` int NOT NULL DEFAULT '0' COMMENT '更新邮件数',
  `deleted_emails` int NOT NULL DEFAULT '0' COMMENT '删除邮件数',
  `error_message` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '错误信息',
  `sync_type` enum('FULL','INCREMENT') NOT NULL DEFAULT 'INCREMENT' COMMENT '同步类型',
  `datetime` datetime NOT NULL COMMENT '同步时间',
  PRIMARY KEY (`id`),
  KEY `idx_account_id` (`account_id`),
  KEY `idx_start_time` (`start_time`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_sync_logs_account_id` FOREIGN KEY (`account_id`) REFERENCES `email_accounts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮件同步日志表';

SET FOREIGN_KEY_CHECKS = 1; 