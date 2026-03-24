import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import UnpinAllMessagesRequest
from telethon.tl.types import MessageService, MessageActionPinMessage

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
    await event.reply("Clearing all pins and pin notifications...")
    try:
        await bot(UnpinAllMessagesRequest(peer=chat))
        deleted = 0
        async for message in bot.iter_messages(chat, limit=None):
            if isinstance(message, MessageService) and isinstance(message.action, MessageActionPinMessage):
                try:
                    await bot.delete_messages(chat, message.id)
                    deleted += 1
                    await asyncio.sleep(0.1)
                except Exception as e:
                    print(f"Failed to delete {message.id}: {e}")
        await event.reply(f"Done! All pins removed and {deleted} pin notification(s) deleted.")
    except Exception as e:
        await event.reply(f"Error: {e}")

@bot.on(events.NewMessage(pattern='/deleteallpins'))
async def delete_all_pinned_posts(event):
    if not event.is_channel:
        await event.reply("This command only works in channels.")
        return
    chat = await event.get_chat()
    await event.reply("Deleting all pinned posts and pin notifications...")
    try:
        deleted_posts = 0
        pinned_msg_ids = []
        async for message in bot.iter_messages(chat, limit=None):
            if hasattr(message, 'pinned') and message.pinned:
                pinned_msg_ids.append(message.id)
        if pinned_msg_ids:
            await bot.delete_messages(chat, pinned_msg_ids)
            deleted_posts = len(pinned_msg_ids)
        await bot(UnpinAllMessagesRequest(peer=chat))
        deleted_notifications = 0
        async for message in bot.iter_messages(chat, limit=None):
            if isinstance(message, MessageService) and isinstance(message.action, MessageActionPinMessage):
                try:
                    await bot.delete_messages(chat, message.id)
                    deleted_notifications += 1
                    await asyncio.sleep(0.1)
                except Exception as e:
                    print(f"Failed to delete {message.id}: {e}")
        await event.reply(f"Done! Deleted {deleted_posts} pinned post(s) and {deleted_notifications} pin notification(s).")
    except Exception as e:
        await event.reply(f"Error: {e}")

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
