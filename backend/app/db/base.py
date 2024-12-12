# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.admin import Admin  # noqa
from app.models.verification_code import VerificationCode  # noqa
from app.models.llm_model import LLMModel  # noqa
from app.models.llm_channel import LLMChannel  # noqa
from app.models.email_provider import EmailProvider  # noqa
from app.models.email_account import EmailAccount  # noqa
