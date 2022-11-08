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


def ucpname(name):
    """
    Check a user UCP Name.

    Args:
        *name: The Username to check for
    """
    regex = r"^[a-zA-Z0-9]{3,15}$"
    p = re.compile(regex)
    if(name == None):
        return False
    if(re.search(p, name)):
        return True
    else:
        return False