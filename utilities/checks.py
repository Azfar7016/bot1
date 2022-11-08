import re
from typing import Awaitable, Callable

from naff import Permissions
from naff.models.naff.context import Context

TYPE_CHECK_FUNCTION = Callable[[Context], Awaitable[bool]]


def member_permissions(*permissions: Permissions) -> TYPE_CHECK_FUNCTION:
    """
    Check if member has any of the given permissions.

    Args:
        *permissions: The Permission(s) to check for
    """

    async def check(ctx: Context) -> bool:
        if ctx.guild is None:
            return False
        if any(ctx.author.has_permission(p) for p in permissions):
            return True

    return check
