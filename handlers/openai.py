import asyncio
import os

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from openai import AsyncOpenAI

from config import OPENAI_KEY
from keyboards.inline import MyCallback, BACK_TO_START
from handlers.State import StepsForm
from database import Database

client = AsyncOpenAI(api_key=OPENAI_KEY)
db = Database()


ASSISTANT_ID = 'asst_08F9ekwGMSufmLHcaVwO2it9'


async def openai(call: CallbackQuery, state: FSMContext):
    await state.clear()

    await call.message.delete()
    await call.message.answer(
        text='Хорошо, анкету можно будет заполнить командой /info.\n\nРасскажи как у тебя дела, как проходит твой день? Пришли мне текст, кружок, или голосовое.'    )

    await state.set_state(StepsForm.text_request)


async def request(message: Message, assistant_id, prompt):
    usage = db.select_usage(message.chat.id)

    if usage > 0:
        threat_id = db.select_thread_id(message.chat.id)

        if threat_id == '0':
            thread = await client.beta.threads.create()

            thread_id = thread.id
            db.update_thread_id(message.chat.id, thread=thread.id)
        else:
            thread_id = threat_id

        usage = usage - 1

        db.update_usage(user_id=message.chat.id,
                        usage=usage)

        message_openai = await client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt
        )

        main_text = ''

        info = db.select_personal_info(user_id=message.chat.id)

        async with client.beta.threads.runs.stream(
                thread_id=thread_id,
                assistant_id=assistant_id,
                instructions=f'Пользователь {info[0]}, обращайся к нему по имени {info[1]}. Ему {info[2]} лет. Дополнительная информация о пользователе: {info[3]}. Тебе нужно обязательно затянуть его в диалог.'
        ) as stream:
            async for text in stream.text_deltas:
                main_text += text

                try:
                    await message.edit_text(text=main_text)
                except:
                    pass

    else:
        await message.edit_text(text='*У вас не имеется подписка на данный момент в боте.*\n\n_Можете купить ее по команде /pay_')


async def chat4(message: Message, state: FSMContext, bot: Bot):
    user_id = message.chat.id

    if message.voice:
        try:
            file_id = message.voice.file_id
        except:
            file_id = message.audio.file_id

        file = await bot.get_file(file_id)
        file_path = file.file_path

        await bot.download_file(file_path, f"files/{message.chat.id}.mp3")

        audio_file = open(f'files/{message.chat.id}.mp3', 'rb')
        transcript = await client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            prompt='Ответь на это сообщение!'
        )

        os.remove(f"files/{message.chat.id}.mp3")

        prompt = transcript.text
    elif message.text:
        prompt = message.text
    elif message.video_note:
        file_id = message.video_note.file_id

        file = await bot.get_file(file_id)
        file_path = file.file_path

        await bot.download_file(file_path, f"files/{message.chat.id}.mp3")

        audio_file = open(f'files/{message.chat.id}.mp3', 'rb')
        transcript = await client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            prompt='Ответь на это сообщение!'
        )

        os.remove(f"files/{message.chat.id}.mp3")

        prompt = transcript.text

    msg = await message.answer('⌛️')
    await bot.send_chat_action(user_id, 'typing')

    await request(msg, assistant_id=ASSISTANT_ID, prompt=prompt)


def router(rt: Router):
    rt.callback_query.register(openai, MyCallback.filter(F.call == 'openai'))
    rt.message.register(chat4, StepsForm.text_request)
