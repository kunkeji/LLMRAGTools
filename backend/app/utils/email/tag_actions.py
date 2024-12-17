"""
邮件标签动作操作工具
"""
from enum import Enum
from typing import List, Dict

class TagAction(str, Enum):
    """标签动作枚举"""
    NO_OPERATION = "no_operation"  # 无操作
    MARK_READ = "mark_read"  # 标记已读
    MARK_UNREAD = "mark_unread"  # 标记未读
    MARK_IMPORTANT = "mark_important"  # 标记重要
    MARK_UNIMPORTANT = "mark_unimportant"  # 取消标记重要
    ARCHIVE = "archive"  # 归档
    UNARCHIVE = "unarchive"  # 取消归档
    MOVE_TO_TRASH = "move_to_trash"  # 移动到垃圾箱
    RESTORE_FROM_TRASH = "restore_from_trash"  # 从垃圾箱恢复

def get_all_actions() -> List[Dict[str, str]]:
    """
    获取所有可用的标签动作列表
    
    Returns:
        List[Dict[str, str]]: 动作列表，每个动作包含名称、动作名称和描述
    """
    actions = [
        {
            "name": "无操作",
            "action_name": TagAction.NO_OPERATION,
            "description": "不执行任何操作"
        },
        {
            "name": "标记已读",
            "action_name": TagAction.MARK_READ,
            "description": "将邮件标记为已读状态"
        },
        {
            "name": "标记未读",
            "action_name": TagAction.MARK_UNREAD,
            "description": "将邮件标记为未读状态"
        },
        {
            "name": "标记重要",
            "action_name": TagAction.MARK_IMPORTANT,
            "description": "将邮件标记为重要"
        },
        {
            "name": "取消重要标记",
            "action_name": TagAction.MARK_UNIMPORTANT,
            "description": "取消邮件的重要标记"
        },
        {
            "name": "归档",
            "action_name": TagAction.ARCHIVE,
            "description": "将邮件移动到归档文件夹"
        },
        {
            "name": "取消归档",
            "action_name": TagAction.UNARCHIVE,
            "description": "将邮件从归档文件夹恢复"
        },
        {
            "name": "移动到垃圾箱",
            "action_name": TagAction.MOVE_TO_TRASH,
            "description": "将邮件移动到垃圾箱"
        },
        {
            "name": "从垃圾箱恢复",
            "action_name": TagAction.RESTORE_FROM_TRASH,
            "description": "将邮件从垃圾箱恢复"
        }
    ]
    return actions