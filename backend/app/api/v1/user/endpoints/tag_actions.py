"""
标签动作相关接口
"""
from fastapi import APIRouter
from app.schemas.response import response_success
from app.utils.email.tag_actions import get_all_actions

router = APIRouter()

@router.get("/actions", summary="获取所有可用的标签动作")
def get_tag_actions() -> dict:
    """
    获取所有可用的标签动作列表
    
    返回:
    - 动作列表，每个动作包含:
        - name: 动作名称
        - action_name: 动作标识符
        - description: 动作描述
    """
    actions = get_all_actions()
    return response_success(data=actions) 