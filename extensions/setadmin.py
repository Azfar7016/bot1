import datetime
import logging
import os
from typing import Optional

import naff
import pymysql.cursors
from dotenv import load_dotenv
from naff import (
    Embed,
    Extension,
    OptionTypes,
    SlashCommandChoice,
    check,
    slash_command,
    slash_option,
)

from utilities.checks import *

load_dotenv()


class setadmin(Extension):
    @slash_command(
        "set-admin",
        description="Set a player admin level",
    )
    @slash_option(
        name="member",
        description="The target @member",
        required=True,
        opt_type=OptionTypes.USER,
    )
    @slash_option(
        name="level",
        description="Admin level you want to promote",
        required=True,
        opt_type=OptionTypes.INTEGER,
        choices=[
            SlashCommandChoice(name="Player", value=0),
            SlashCommandChoice(name="Junior Helper", value=1),
            SlashCommandChoice(name="Senior Helper", value=2),
            SlashCommandChoice(name="Administrator", value=3),
            SlashCommandChoice(name="High Administrator", value=4),
            SlashCommandChoice(name="Supervisor", value=5),
            SlashCommandChoice(name="Management", value=6),
            SlashCommandChoice(name="Discord Manager", value=7),
            SlashCommandChoice(name="Developer", value=8),
        ],
    )
    @slash_option(
        "reason",
        "The reason of promote/demote",
        OptionTypes.STRING,
        required=False,
    )
    @check(member_permissions(Permissions.ADMINISTRATOR))
    async def set_admin(
        self,
        ctx,
        member: naff.Member,
        level: int,
        reason: Optional[str] = "No reason provided",
    ):
        await ctx.defer()

        # Connect to the database
        connection = pymysql.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME"),
            cursorclass=pymysql.cursors.DictCursor,
        )

        if member.bot:
            embed = Embed(
                description=f":x: You can't promote/demote discord bot!",
                color=0xFF0000,
            )
            await ctx.send(embed=embed, ephemeral=True)
            return

        try:
            with connection:
                with connection.cursor() as cursor:
                    # check if user is already registered
                    sql = f"SELECT `DiscordID` FROM `accounts` WHERE `DiscordID`=%s"
                    cursor.execute(sql, (member.id))
                    result = cursor.fetchone()

                    if result is not None:
                        # get channel to send the logs
                        w = self.bot.get_channel(1037665413183578143)

                        # update records to database
                        sql = "UPDATE `accounts` SET `Admin` = %s WHERE `accounts`.`DiscordID` = %s"
                        cursor.execute(sql, (level, f"{member.id}"))

                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                        connection.commit()

                        # add level checks
                        if level == 0:
                            rank = "Player"
                        if level == 1:
                            rank = "Junior Helper"
                        if level == 2:
                            rank = "Senior Helper"
                        if level == 3:
                            rank = "Administrator"
                        if level == 4:
                            rank = "High Administrator"
                        if level == 5:
                            rank = "Supervisor"
                        if level == 6:
                            rank = "Management"
                        if level == 7:
                            rank = "Discord Manager"
                        if level == 8:
                            rank = "Developer"

                        # send embed to ucp-logs
                        embed = Embed(title="User Promoted/Demoted", color=0x00FF00)
                        embed.add_field(name="New Rank:", value=rank, inline=True)
                        embed.add_field(
                            name="Responsible Admin:",
                            value=ctx.author.mention,
                            inline=True,
                        )
                        embed.add_field(name="Reason:", value=reason, inline=False)
                        embed.set_author(
                            name=f"{member.username}#{member.discriminator}",
                            url=f"https://discordapp.com/users/{member.id}",
                            icon_url=member.avatar.url,
                        )
                        embed.set_footer(
                            text=f"{ctx.guild.name} | User ID: {member.id}",
                            icon_url=ctx.guild.icon.url,
                        )
                        embed.timestamp = datetime.datetime.utcnow()
                        await w.send(embed=embed)

                        # notify user the changes
                        try:
                            await member.send(
                                f"You have been promoted/demoted to `{rank}` by {ctx.author.mention}\nReason: {reason}"
                            )
                            await ctx.send(
                                f"Successfully promoted/demoted {member.mention}\n\nI already notified the user about the changes.",
                                ephemeral=True,
                            )
                        except:
                            logging.info(f"Can't send message to {ctx.author} :(")
                            await ctx.send(
                                f"Successfully promoted/demoted {member.mention}\n\nUnfortunately i can't notify the user about the changes because their server dm's are closed :(",
                                ephemeral=True,
                            )
                    else:
                        # send error message if user is not found
                        await ctx.send(
                            "Invalid user!",
                            ephemeral=True,
                        )
        except:
            connection.close()


def setup(bot):
    # This is called by dis-snek so it knows how to load the Scale
    setadmin(bot)
