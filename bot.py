import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import UnpinAllMessagesRequest

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
    await event.reply("Clearing all pins...")
    try:
        await bot(UnpinAllMessagesRequest(peer=chat))
        await event.reply("Done! All pins have been removed.")
    except Exception as e:
        await event.reply(f"Error: {e}")

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
