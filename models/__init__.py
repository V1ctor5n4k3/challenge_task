# Importa todos los modelos aquí para que Alembic los detecte
from db.base import Base
from .users import User
from .posts import Posts
from .tags import Tags
from .comments import Comments

# Lista explícita para Alembic
__all__ = ["Base", "User", "Posts", "Tags", "Comments"]