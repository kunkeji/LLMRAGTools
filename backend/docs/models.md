# 数据库模型文档

## 用户相关模型

### User (用户)
```sql
CREATE TABLE user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50),
    avatar VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Admin (管理员)
```sql
CREATE TABLE admin (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### VerificationCode (验证码)
```sql
CREATE TABLE verification_code (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL,
    type VARCHAR(20) NOT NULL,
    expired_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 邮件相关模型

### EmailProvider (邮件服务商)
```sql
CREATE TABLE email_provider (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    imap_host VARCHAR(100) NOT NULL,
    imap_port INT NOT NULL,
    smtp_host VARCHAR(100) NOT NULL,
    smtp_port INT NOT NULL,
    use_ssl BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### EmailAccount (邮箱账户)
```sql
CREATE TABLE email_account (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    provider_id BIGINT NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_encrypted VARCHAR(255) NOT NULL,
    name VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (provider_id) REFERENCES email_provider(id)
);
```

### Email (邮件)
```sql
CREATE TABLE email (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_id BIGINT NOT NULL,
    message_id VARCHAR(255) NOT NULL,
    from_address VARCHAR(100) NOT NULL,
    to_address TEXT NOT NULL,
    cc_address TEXT,
    bcc_address TEXT,
    subject VARCHAR(255),
    content TEXT,
    html_content TEXT,
    received_at DATETIME NOT NULL,
    folder VARCHAR(50) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    is_starred BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES email_account(id)
);
```

### EmailTag (邮件标签)
```sql
CREATE TABLE email_tag (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### EmailTagMapping (邮件标签映射)
```sql
CREATE TABLE email_tag_mapping (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email_id) REFERENCES email(id),
    FOREIGN KEY (tag_id) REFERENCES email_tag(id)
);
```

### EmailOutbox (发件箱)
```sql
CREATE TABLE email_outbox (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_id BIGINT NOT NULL,
    to_address TEXT NOT NULL,
    cc_address TEXT,
    bcc_address TEXT,
    subject VARCHAR(255),
    content TEXT,
    html_content TEXT,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    retry_count INT DEFAULT 0,
    next_retry_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES email_account(id)
);
```

## LLM相关模型

### LLMModel (AI模型)
```sql
CREATE TABLE llm_model (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    type VARCHAR(20) NOT NULL,
    config JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### LLMChannel (渠道)
```sql
CREATE TABLE llm_channel (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    model_id BIGINT NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    config JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES llm_model(id)
);
```

### LLMFeature (特性)
```sql
CREATE TABLE llm_feature (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    type VARCHAR(20) NOT NULL,
    config JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### LLMFeatureMapping (特性映射)
```sql
CREATE TABLE llm_feature_mapping (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    channel_id BIGINT NOT NULL,
    feature_id BIGINT NOT NULL,
    config JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES llm_channel(id),
    FOREIGN KEY (feature_id) REFERENCES llm_feature(id)
);
```

## 其他模型

### Document (文档)
```sql
CREATE TABLE document (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(20) NOT NULL,
    size BIGINT NOT NULL,
    path VARCHAR(255) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Task (任务)
```sql
CREATE TABLE task (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    schedule VARCHAR(100),
    config JSON,
    last_run_at DATETIME,
    next_run_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Log (系统日志)
```sql
CREATE TABLE log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    type VARCHAR(20) NOT NULL,
    action VARCHAR(50) NOT NULL,
    content TEXT,
    ip VARCHAR(50),
    user_agent VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
``` 