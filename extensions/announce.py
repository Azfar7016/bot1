# Credits to Discord-Snake-Pit/Dis-secretary

from naff.models import Extension, GuildNews, Message, listen
import logging


class announce(Extension):
    @listen()
    async def on_message_create(self, event):
        message: Message = event.message
        if isinstance(message.channel, GuildNews):
            try:
                await message.publish()
            except Exception:
                logging.warn("message publish failed")
                pass
            else:
                logging.info("message publish succeeded")


def setup(bot):
    announce(bot)
