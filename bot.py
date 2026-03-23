from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelFull, Message

API_ID = 33017187
API_HASH = '31ffa8744c33d4e7e537beddeb6dcb6a'
BOT_TOKEN = '8623951994:AAEIfOwCsa61Ti8ROb24p8d4l0jnZ8IpAuI'

client = TelegramClient('ghost_pin_cleaner_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/clearpins', forwards=False, outgoing=False))
async def clear_ghost_pins(event):
    if not event.is_channel:
        return
    chat = await event.get_chat()
    sender = await event.get_sender()
    is_admin = False
    if event.is_group or event.is_channel:
        participants = await client.get_participants(chat, filter=None)
        for p in participants:
            if p.id == sender.id and (p.admin_rights or p.creator):
                is_admin = True
                break
    if not is_admin:
        await event.reply("You need to be an administrator to use this command.")
        return
    await event.reply("Scanning for ghost pins...")
    try:
        full_channel = await client(GetFullChannelRequest(channel=chat))
        pinned_messages_ids = full_channel.full_chat.pinned_msg_ids
        if not pinned_messages_ids:
            await event.reply("No pinned messages found in this channel.")
            return
        ghost_pins_removed_count = 0
        for msg_id in pinned_messages_ids:
            try:
                message = await client.get_messages(chat, ids=msg_id)
                if message is None or isinstance(message, Message) and message.media is None and message.message is None:
                    await client.unpin_message(chat, message=msg_id)
                    ghost_pins_removed_count += 1
                    await asyncio.sleep(0.1)
            except Exception as e:
                try:
                    await client.unpin_message(chat, message=msg_id)
                    ghost_pins_removed_count += 1
                except:
                    pass
        if ghost_pins_removed_count > 0:
            await event.reply(f"Successfully unpinned {ghost_pins_removed_count} ghost pin(s).")
        else:
            await event.reply("No ghost pins found.")
    except Exception as e:
        await event.reply(f"An error occurred: {e}")

async def main():
    print("Bot started. Listening for commands...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
