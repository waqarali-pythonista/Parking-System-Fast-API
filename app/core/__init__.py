# app/core/__init__.py

# This file can be left empty or used to import core utilities to make them accessible at the package level.
# By importing core utilities here, we can use `from app.core import security, config` elsewhere in the application.

from .security import get_current_user, create_access_token, hash_password, verify_password
from .config import SECRET_KEY, ALGORITHM
from .utils import send_email
