-- 修改 reply_type 枚举类型
ALTER TABLE email_outbox MODIFY COLUMN reply_type ENUM('pre_reply', 'auto_reply', 'manual_reply', 'quick_reply'); 