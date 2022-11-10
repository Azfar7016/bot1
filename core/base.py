import logging
import os

from naff import Client, listen, logger_name


class CustomClient(Client):
    """Subclass of naff.Client with our own logger and on_startup event"""

    # you can use that logger in all your extensions
    logger = logging.getLogger(logger_name)

    @listen()
    async def on_startup(self):
        """Gets triggered on startup"""

        self.logger.info(f"{os.getenv('PROJECT_NAME')} - Startup Finished!")
        self.logger.info(
            "Note: Discord needs up to an hour to load your global commands / context menus. They may not appear immediately\n"
        )

    async def on_command_error(self, ctx, error):
        """Gets triggered on a command error"""
        if isinstance(error, CommandCheckFailure):
            if isinstance(ctx, InteractionContext):
                symbol = "/"

            await ctx.send(
                embeds=Embed(
                    description="<:cross:839158779815657512> I'm afraid I can't let you use that",
                    color=0xFF0000,
                ),
                ephemeral=True,
            )
            self.logger.warning(
                f"Check failed on Command: [{symbol}{ctx.invoke_target}]"
            )

        elif isinstance(error, CommandOnCooldown):
            if isinstance(ctx, InteractionContext):
                symbol = "/"

            await ctx.send(
                embeds=Embed(
                    description=f"<:cross:839158779815657512> Cooldown is active for this command. You'll be able to use it in {int(error.cooldown.get_cooldown_time())} seconds",
                    color=0xFF0000,
                ),
                ephemeral=True,
            )
            self.logger.warning(
                f"Command Ratelimited for {int(error.cooldown.get_cooldown_time())} seconds on: [{symbol}{ctx.invoke_target}]"
            )

        elif isinstance(error, HTTPException):
            if isinstance(ctx, InteractionContext):
                symbol = "/"

                await ctx.send(
                    embeds=Embed(
                        description=f"<:cross:839158779815657512> Something happened while trying to process your request, Please try again later!",
                        color=0xFF0000,
                    ),
                    ephemeral=True,
                )
