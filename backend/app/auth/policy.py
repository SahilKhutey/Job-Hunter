from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    AGENT = "agent" # Service-to-service identity

class Permission(str, Enum):
    READ_ALL = "read:all"
    WRITE_ALL = "write:all"
    EXECUTE_AUTOMATION = "execute:automation"
    READ_OWN = "read:own"

ROLE_PERMISSIONS = {
    Role.ADMIN: [Permission.READ_ALL, Permission.WRITE_ALL, Permission.EXECUTE_AUTOMATION],
    Role.USER: [Permission.READ_OWN, Permission.EXECUTE_AUTOMATION],
    Role.AGENT: [Permission.EXECUTE_AUTOMATION]
}

class PolicyEngine:
    @staticmethod
    def can_access(user_role: Role, required_permission: Permission) -> bool:
        permissions = ROLE_PERMISSIONS.get(user_role, [])
        return required_permission in permissions

    @staticmethod
    def is_owner(user_id: str, resource_owner_id: str) -> bool:
        return user_id == resource_owner_id
