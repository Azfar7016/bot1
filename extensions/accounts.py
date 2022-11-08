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
    Modal,
    ShortText,
)

import random

load_dotenv()


class accounts(Extension):
    @slash_command(
        "register",
        description="Register your UCP account",
    )
    async def register(
        self,
        ctx,
    ):
        try:
            # Connect to the database
            connection = pymysql.connect(
                host=os.getenv("DATABASE_HOST"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
                database=os.getenv("DATABASE_NAME"),
                cursorclass=pymysql.cursors.DictCursor,
            )
            with connection:
                with connection.cursor() as cursor:
                    # check if user is already registered
                    sql = f"SELECT `DiscordID` FROM `accounts` WHERE `DiscordID`=%s"
                    cursor.execute(sql, (ctx.author.id))
                    result = cursor.fetchone()

                    if result is None:
                        my_modal = Modal(
                            title="Register UCP Clavaria Roleplay",
                            components=[
                                ShortText(
                                    label="Username",
                                    custom_id="username",
                                    placeholder="Masukkan Username UCP kamu, BUKAN NAMA CHARACTER! (contoh: Firpanpus, Bebeg, Kentank)",
                                    required=True,
                                ),
                            ],
                        )
                        await ctx.send_modal(modal=my_modal)  # send modal to users

                        # wait for user to enter the credentials
                        modal_ctx: ModalContext = await self.bot.wait_for_modal(
                            my_modal
                        )

                        # get channel to send the logs
                        w = self.bot.get_channel(1037665413183578143)

                        # generate random numbers for verification code
                        number = random.randint(1000, 9999)

                        # get modal responses
                        user = modal_ctx.responses["username"]

                        # add records to database
                        sql = "INSERT INTO `accounts` (`Username`, `VerifyCode`, `DiscordID`) VALUES (%s, %s, %s)"
                        cursor.execute(
                            sql, (f"{user}", f"{number}", f"{ctx.author.id}")
                        )

                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                        connection.commit()

                        # send embed to ucp-logs
                        embed = Embed(title="New User Registered!", color=0x00FF00)
                        embed.add_field(name="Username:", value=user, inline=True)
                        embed.add_field(name="Verify Code:", value=f"||{number}||", inline=True)
                        embed.set_author(
                            name=f"{ctx.author.username}#{ctx.author.discriminator}",
                            url=f"https://discordapp.com/users/{ctx.author.id}",
                            icon_url=ctx.author.avatar.url,
                        )
                        embed.set_thumbnail(url=ctx.author.avatar.url)
                        embed.set_footer(
                            text=f"{ctx.guild.name} | User ID: {ctx.author.id}",
                            icon_url=ctx.guild.icon.url,
                        )
                        embed.timestamp = datetime.datetime.utcnow()
                        await w.send(embed=embed)

                        # add ucp registered role to user
                        verified_id = 984084468195295302
                        unverified_id = 984084342097727548
                        await ctx.author.add_role(
                            verified_id,
                            f"{user} just Registered, gave'em the Verified role..",
                        )
                        await ctx.author.remove_role(
                            unverified_id,
                            f"{user} Removed the Unverified role..",
                        )

                        # send username & verification code to user for safekeeping
                        manusya = Embed(
                            description="**Your New UCP Account**", color=0x17A168
                        )
                        manusya.add_field(
                            name="Username:", value=f"||{user}||", inline=True
                        )
                        manusya.add_field(
                            name="Verification Code:",
                            value=f"||{number}||",
                            inline=False,
                        )
                        try:
                            await ctx.author.send(embed=manusya)
                            await modal_ctx.send(
                                "Thank you for registering!\n\nCheck your DM's for your new username & verification code!",
                                ephemeral=True,
                            )
                        except:
                            logging.info(f"Can't send message to {ctx.author} :(")
                            await modal_ctx.send(
                                "Thank you for registering!\n\nUnfortunately your server dm's are closed and we can't send your new username & verification code to you. Please open your server dm's and try again.",
                                ephemeral=True,
                            )
                        # send modal responses
                    else:
                        # send error message if user already registered
                        await ctx.send(
                            "You're already registered! (1 UCP account per discord user)\nIf you're having trouble, contact an admin.",
                            ephemeral=True,
                        )
        except:
            connection.close()
        
    
    @slash_command(
        "resend",
        description="Resend your UCP verification code to your dm's",
    )
    async def resend(
        self,
        ctx,
    ):
        await ctx.defer()
        try:
            # Connect to the database
            connection = pymysql.connect(
                host=os.getenv("DATABASE_HOST"),
                user=os.getenv("DATABASE_USER"),
                password=os.getenv("DATABASE_PASSWORD"),
                database=os.getenv("DATABASE_NAME"),
                cursorclass=pymysql.cursors.DictCursor,
            )
            with connection:
                with connection.cursor() as cursor:
                    # check if user is already registered
                    sql = f"SELECT * FROM `accounts` WHERE `DiscordID`=%s"
                    cursor.execute(sql, (ctx.author.id))
                    result = cursor.fetchone()

                    if result is not None:
                        # send username & verification code to user for safekeeping
                        user = result["Username"]
                        number = result["VerifyCode"]

                        manusya = Embed(
                            description="**Your New UCP Account**", color=0x17A168
                        )
                        manusya.add_field(
                            name="Username:", value=f"||{user}||", inline=True
                        )
                        manusya.add_field(
                            name="Verification Code:",
                            value=f"||{number}||",
                            inline=False,
                        )
                        try:
                            await ctx.author.send(embed=manusya)
                            await ctx.send(
                                "Your username & verification code has been re-sended, Check your DM's!",
                                ephemeral=True,
                            )
                        except:
                            logging.warn(f"Can't send message to {ctx.author} :(")
                            await ctx.send(
                                "Your server dm's still closed and we can't send your username & verification code to you. Please open your server dm's and try again.",
                                ephemeral=True,
                            )
                        # send modal responses
                    else:
                        # send error message if user already registered
                        await ctx.send(
                            "You're not registered yet! Please use </register:1039400721319198741> to register.",
                            ephemeral=True,
                        )
        except:
            connection.close()


def setup(bot):
    # This is called by dis-snek so it knows how to load the Scale
    accounts(bot)
