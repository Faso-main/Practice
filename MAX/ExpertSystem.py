import asyncio
from maxapi import Bot, Dispatcher, F
from maxapi.types import MessageCreated

bot = Bot('token________________________________')
dp = Dispatcher()

# Хранение состояния опроса для каждого пользователя в памяти
user_states = {}

questions = [
    {
        "question": "Какой у вас опыт работы?",
        "options": ["Меньше года", "От 1 до 3 лет", "Больше 3 лет"]
    },
    {
        "question": "Интересует ли вас удалённая работа?",
        "options": ["Да", "Нет"]
    }
]

def expert_system(answers):
    if answers[0] == 1 and answers[1] == 2:
        return "Рекомендуется вариант A."
    elif answers[0] == 2:
        return "Стоит рассмотреть вариант B."
    else:
        return "Требуются дополнительные данные для рекомендации."

@dp.message_created(F.message.body.text)
async def handle_message(event: MessageCreated):
    user_id = event.message.sender.id
    text = event.message.body.text.strip()

    if user_id not in user_states:
        # Начинаем опрос
        user_states[user_id] = {"step": 0, "answers": []}
        q = questions[0]
        options_text = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(q["options"]))
        await event.message.answer(f"{q['question']}\n{options_text}")
        return

    state = user_states[user_id]
    step = state["step"]
    q = questions[step]

    # Проверяем корректность ответа
    if not text.isdigit() or not (1 <= int(text) <= len(q["options"])):
        options_text = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(q["options"]))
        await event.message.answer(f"Пожалуйста, выберите номер варианта из списка:\n{options_text}")
        return

    # Сохраняем ответ и переходим к следующему вопросу или заканчиваем
    state["answers"].append(int(text))
    state["step"] += 1

    if state["step"] < len(questions):
        next_q = questions[state["step"]]
        options_text = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(next_q["options"]))
        await event.message.answer(f"{next_q['question']}\n{options_text}")
    else:
        result = expert_system(state["answers"])
        await event.message.answer(f"Результат опросника: {result}")
        # Очищаем состояние пользователя после завершения опроса
        del user_states[user_id]

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt: print('Остановлено в ручную')
    except Exception as e: print(f'Ошибка вида: {e}')
