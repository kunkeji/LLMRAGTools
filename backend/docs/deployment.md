# 部署文档

## 系统要求

### 硬件要求
- CPU: 4核心及以上
- 内存: 8GB及以上
- 硬盘: 50GB及以上（取决于数据量）

### 软件要求
- Python 3.8+
- MySQL 5.7+
- Redis 6.0+
- Nginx 1.18+（用于反向代理）

## 部署步骤

### 1. 环境准备

#### 安装系统依赖
```bash
# Ubuntu/Debian
apt-get update
apt-get install -y python3-pip python3-venv mysql-server redis-server nginx

# CentOS/RHEL
yum update
yum install -y python3-pip python3-venv mysql-server redis nginx
```

#### 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # Linux
.\venv\Scripts\activate   # Windows
```

#### 安装 Python 依赖
```bash
pip install -r requirements.txt
```

### 2. 数据库配置

#### 创建数据库
```sql
CREATE DATABASE agent_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'agent'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON agent_db.* TO 'agent'@'localhost';
FLUSH PRIVILEGES;
```

#### 执行数据库迁移
```bash
alembic upgrade head
```

### 3. Redis 配置

编辑 Redis 配置文件 `/etc/redis/redis.conf`：
```conf
bind 127.0.0.1
port 6379
maxmemory 2gb
maxmemory-policy allkeys-lru
```

### 4. 应用配置

#### 环境变量
复制并编辑环境变量文件：
```bash
cp .env.example .env
```

主要配置项：
```bash
# 数据库配置
DATABASE_URL=mysql+pymysql://agent:your_password@localhost:3306/agent_db

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# 应用配置
RUN_MODE=prod
PORT=8111
LOG_LEVEL=INFO

# JWT 配置
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# SMTP 配置
SMTP_HOST=smtp.example.com
SMTP_PORT=465
SMTP_USER=your-email
SMTP_PASSWORD=your-password

# LLM API 配置
OPENAI_API_KEY=your-api-key
ANTHROPIC_API_KEY=your-api-key
ZHIPU_API_KEY=your-api-key
```

### 5. Nginx 配置

创建 Nginx 配置文件 `/etc/nginx/sites-available/LLMRAGTools`：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8111;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/static;
        expires 30d;
    }

    location /uploads {
        alias /path/to/your/uploads;
        expires 30d;
    }
}
```

启用配置：
```bash
ln -s /etc/nginx/sites-available/LLMRAGTools /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 6. 服务配置

#### Systemd 服务
创建服务文件 `/etc/systemd/system/LLMRAGTools.service`：
```ini
[Unit]
Description=LLMRAGTools Backend Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/backend
Environment="PATH=/path/to/your/venv/bin"
EnvironmentFile=/path/to/your/.env
ExecStart=/path/to/your/venv/bin/python run.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
systemctl daemon-reload
systemctl enable LLMRAGTools
systemctl start LLMRAGTools
```

## 维护指南

### 1. 日志管理

#### 日志位置
- 应用日志: `logs/api.log`
- Nginx 日志: `/var/log/nginx/`
- MySQL 日志: `/var/log/mysql/`

#### 日志轮转
配置 logrotate：
```conf
/path/to/your/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload LLMRAGTools
    endscript
}
```

### 2. 备份策略

#### 数据库备份
创建备份脚本 `backup.sh`：
```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
MYSQL_USER="agent"
MYSQL_PASS="your_password"
DB_NAME="agent_db"

# 创建备份
mysqldump -u$MYSQL_USER -p$MYSQL_PASS $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# 保留最近30天的备份
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +30 -delete
```

添加到 crontab：
```bash
0 2 * * * /path/to/backup.sh
```

#### 文件备份
```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/path/to/your/backend"

# 备份上传文件和配置
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz $APP_DIR/uploads $APP_DIR/.env

# 保留最近30天的备份
find $BACKUP_DIR -name "files_backup_*.tar.gz" -mtime +30 -delete
```

### 3. 监控

#### 系统监控
使用 Prometheus + Grafana：

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'LLMRAGTools'
    static_configs:
      - targets: ['localhost:8111']
```

#### 应用监控
添加健康检查端点：
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": await check_database(),
        "redis": await check_redis(),
        "version": "1.0.0"
    }
```

### 4. 性能优化

#### MySQL 优化
```ini
[mysqld]
innodb_buffer_pool_size = 4G
innodb_log_file_size = 512M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT
```

#### Redis 优化
```conf
maxmemory 4gb
maxmemory-policy volatile-lru
```

#### 应用优化
```python
# 配置连接池
DATABASE_CONFIG = {
    "pool_size": 20,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 1800
}
```

### 5. 故障处理

#### 1. 服务无响应
```bash
# 检查服务状态
systemctl status LLMRAGTools

# 检查日志
tail -f logs/api.log

# 重启服务
systemctl restart LLMRAGTools
```

#### 2. 数据库连接问题
```bash
# 检查数据库状态
systemctl status mysql

# 检查连接
mysql -u agent -p agent_db

# 检查连接数
show processlist;
```

#### 3. Redis 问题
```bash
# 检查 Redis 状态
systemctl status redis

# 检查连接
redis-cli ping

# 监控命令
redis-cli monitor
```

## 升级指南

### 1. 准备工作
```bash
# 备份数据
./backup.sh

# 拉取新代码
git pull origin main
```

### 2. 升级步骤
```bash
# 停止服务
systemctl stop LLMRAGTools

# 更新依赖
pip install -r requirements.txt

# 执行数据库迁移
alembic upgrade head

# 更新静态文件
python manage.py collectstatic

# 启动服务
systemctl start LLMRAGTools
```

### 3. 回滚流程
```bash
# 如果升级失败，回滚代码
git checkout previous-version

# 恢复数据库
mysql -u agent -p agent_db < backup.sql

# 重启服务
systemctl restart LLMRAGTools
```

## 安全建议

1. **系统安全**
   - 及时更新系统补丁
   - 使用防火墙
   - 限制端口访问

2. **应用安全**
   - 使用 HTTPS
   - 实现速率限制
   - 加密敏感数据

3. **数据安全**
   - 定期备份
   - 数据加密
   - 访问控制
