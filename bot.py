from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetFullChannelRequest
import asyncio

API_ID = 33017187
API_HASH = '31ffa8744c33d4e7e537beddeb6dcb6a'
BOT_TOKEN = '8623951994:AAEIfOwCsa61Ti8ROb24p8d4l0jnZ8IpAuI'

bot = TelegramClient('bot', API_ID, API_HASH)

@bot.on(events.NewMessage(pattern='/clearpins'))
async def clear_ghost_pins(event):
    if not event.is_channel:
        await event.reply("This command only works in channels.")
        return
    chat = await event.get_chat()
    await event.reply("Scanning for ghost pins...")
    try:
        full_channel = await bot(GetFullChannelRequest(channel=chat))
        pinned_msg_ids = full_channel.full_chat.pinned_msg_ids
        if not pinned_msg_ids:
            await event.reply("No pinned messages found in this channel.")
            return
        removed = 0
        for msg_id in pinned_msg_ids:
            try:
                msg = await bot.get_messages(chat, ids=msg_id)
                if msg is None:
                    await bot.unpin_message(chat, message=msg_id)
                    removed += 1
                    await asyncio.sleep(0.5)
            except Exception:
                try:
                    await bot.unpin_message(chat, message=msg_id)
                    removed += 1
                    await asyncio.sleep(0.5)
                except Exception:
                    pass
        if removed > 0:
            await event.reply(f"Done! Removed {removed} ghost pin(s).")
        else:
            await event.reply("No ghost pins found.")
    except Exception as e:
        await event.reply(f"Error: {e}")

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
