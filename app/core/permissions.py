from fastapi import Depends, HTTPException, status

from app.models.user import User
from app.core.security import get_current_user
from app.core.role import Role



def require_roles(*roles: Role):
    """
    Authorize the current user against one or more roles.

    Example:

    Depends(require_roles(Role.ADMIN))
    Depends(require_roles(Role.ADMIN, Role.MANAGER))
    """

    role_set = set(roles)

    def _require_roles(current_user: User=Depends(get_current_user)):
        if current_user.role is None or current_user.role not in role_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user

    return _require_roles
