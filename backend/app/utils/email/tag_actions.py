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
    # 预回复
    PRE_REPLY = "pre_reply"  # 预回复
    # 自动回复
    AUTO_REPLY = "auto_reply"  # 自动回复
    # 提醒
    REMIND = "remind"  # 通过微信提醒
    # 移动到垃圾箱
    MOVE_TO_TRASH = "move_to_trash"  # 移动到垃圾箱
    # 删除
    DELETE = "delete"  # 删除

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
            "name": "预回复",
            "action_name": TagAction.PRE_REPLY,
            "description": "预回复邮件"
        },
        {
            "name": "自动回复",
            "action_name": TagAction.AUTO_REPLY,
            "description": "自动回复邮件"
        },
        {
            "name": "提醒",
            "action_name": TagAction.REMIND,
            "description": "通过微信提醒"
        },
        {
            "name": "移动到垃圾箱",
            "action_name": TagAction.MOVE_TO_TRASH,
            "description": "将邮件移动到垃圾箱"
        },
        {
            "name": "删除",
            "action_name": TagAction.DELETE,
            "description": "删除邮件"
        }
    ]
    return actions