# app/__init__.py

# This file can be left empty or used to import core components to make them accessible at the package level.
# For instance, we can use this file to import core utilities like config or database methods, or services.

from .database import engine, Base
from .core.config import SECRET_KEY, ALGORITHM
from .core.security import get_current_user, create_access_token
