-- LLM功能表
CREATE TABLE `llm_features` (
    `feature_type` VARCHAR(50) NOT NULL COMMENT '功能类型',
    `name` VARCHAR(100) NOT NULL COMMENT '功能名称',
    `description` TEXT NULL COMMENT '功能描述',
    `default_prompt` TEXT NOT NULL COMMENT '默认提示词模板',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`feature_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='LLM功能定义表';

-- 初始化功能数据
INSERT INTO `llm_features` (`feature_type`, `name`, `description`, `default_prompt`) VALUES
('DOCUMENT_WRITE', '文档写作', 'AI辅助文档写作', '你是一个专业的文档写作助手。请根据用户的要求，帮助撰写或优化文档内容。要求：\n1. 使用清晰、专业的语言\n2. 结构合理，层次分明\n3. 重点突出，逻辑清晰'),
('DOCUMENT_IMPROVE', '文档改进', '改进现有文档的质量', '你是一个专业的文档优化助手。请根据用户提供的文档内容，从以下几个方面进行优化：\n1. 语言表达是否准确、专业\n2. 结构是否合理、完整\n3. 内容是否存在优化空间\n4. 提供具体的修改建议'),
('DOCUMENT_SUMMARY', '文档总结', '生成文档摘要', '你是一个专业的文档总结助手。请对用户提供的文档内容进行总结：\n1. 提取文档的核心观点和主要内容\n2. 保持总结的简洁性和完整性\n3. 突出重点，忽略细节\n4. 使用清晰的语言组织总结内容'),
('DOCUMENT_TRANSLATE', '文档翻译', '文档多语言翻译', '你是一个专业的文档翻译助手。请按照以下要求进行翻译：\n1. 准确理解原文含义\n2. 保持专业术语的准确性\n3. 翻译后的文本要通顺、自然\n4. 保持原文的格式和结构'),

-- LLM功能映射表
CREATE TABLE `llm_feature_mappings` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '映射ID',
    `user_id` INT NOT NULL COMMENT '用户ID',
    `channel_id` INT NOT NULL COMMENT '渠道ID',
    `feature_type` VARCHAR(50) NOT NULL COMMENT '功能类型',
    `prompt_template` TEXT NULL COMMENT '自定义提示词模板',
    `last_used_at` DATETIME NULL COMMENT '最后使用时间',
    `use_count` INT NOT NULL DEFAULT 0 COMMENT '使用次数',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `deleted_at` DATETIME NULL COMMENT '删除时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_feature` (`user_id`, `feature_type`),
    KEY `idx_feature_type` (`feature_type`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_channel_id` (`channel_id`),
    CONSTRAINT `fk_feature_mappings_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_feature_mappings_channel` FOREIGN KEY (`channel_id`) REFERENCES `llm_channels` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_feature_mappings_feature` FOREIGN KEY (`feature_type`) REFERENCES `llm_features` (`feature_type`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='LLM功能映射表';