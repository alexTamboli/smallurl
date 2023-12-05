from .base import *
import os

if os.environ.get("ENVIRONMENT") == 'Production':
    from .development import *
    # from .production import *
else:
    from .development import *
