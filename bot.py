from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetPinnedMessagesRequest
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
        result = await bot(GetPinnedMessagesRequest(peer=chat))
        all_messages = result.messages
        if not all_messages:
            await event.reply("No pinned messages found in this channel.")
            return
        removed = 0
        for msg in all_messages:
            if msg.__class__.__name__ == 'MessageEmpty' or msg.__class__.__name__ == 'MessageService':
                try:
                    await bot.unpin_message(chat, message=msg.id)
                    removed += 1
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"Failed to unpin {msg.id}: {e}")
        if removed > 0:
            await event.reply(f"Done! Removed {removed} ghost pin(s).")
        else:
            await event.reply("No ghost pins found. All pinned messages are still alive.")
    except Exception as e:
        await event.reply(f"Error: {e}")

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
