from telethon import TelegramClient, events
import asyncio
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji
from telethon.errors import ChatAdminRequiredError  # Добавляем обработку ошибки прав

api_id = 'id'
api_hash = 'hash'
channels = ['@rabotnik_volgograd' , '@rabotnik_novosib' , '@rabotnik_ekat' , '@rabotnik_spb' , '@rabotnik_beta' , '@rabotnik_mo' , '@rabotnik_vakansii_rabota_msk' , '@rabotnik_krasnodar' , '@rabotnik_rostov' , '@rabotnik_samara']

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=channels))
async def react_to_message(event):
    try:
        # Безопасное получение информации о чате
        chat = await client.get_input_entity(event.chat_id)
        msg_id = event.message.id
        
        reactions = ['👍']
        
        for reaction in reactions:
            try:
                await client(SendReactionRequest(
                    peer=chat,
                    msg_id=msg_id,
                    reaction=[ReactionEmoji(emoticon=reaction)]
                ))
                await asyncio.sleep(2)
            except ChatAdminRequiredError:
                print(f"Нет прав для реакций в {event.chat.title}")
                break
            except Exception as ex:
                print(f"Ошибка реакции: {ex}")
                continue
        
        print(f'Успешно обработано сообщение в {event.chat.title}')
    except Exception as e:
        print(f'Критическая ошибка: {e}')

async def main():
    await client.start()
    print("Бот запущен...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())