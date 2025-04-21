import asyncio
import json
from core.agent import async_chat_completion
from integrations.orchestrator import orchestrate_browser_chat

def handle_user_input(user_text: str) -> str:
    text = user_text.lower().strip()
    # список ваших триггеров
    triggers = [
        "обратись к gpt",
        "обратись в gpt",
        "обратись к чпт",
        "у gpt",
        "спроси gpt",
        "спроси чпт",
        "сценарий 1"
    ]
    # ищем первый совпавший триггер
    for trig in triggers:
        if text.startswith(trig):
            query = user_text[len(trig):].strip()  # обрезаем по длине сплошного триггера
            if not query:
                return f"Ошибка: не указан запрос после «{trig}»."
            print(f"Обнаружен триггер «{trig}», запрос: {query}")
            result = orchestrate_browser_chat(query)
            print("Результат оркестрации:", result)
            return "Запрос выполнен через браузер."
    # если ни один триггер не сработал — обычный запрос
    print("Обычный запрос:", user_text)
    return generate_gpt_response(user_text)
    

def generate_gpt_response(text: str) -> str:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(async_chat_completion(text))
    except Exception as e:
        print("Ошибка в generate_gpt_response:", e)
        return json.dumps({"status": 500, "statusMessage": str(e)})
    finally:
        loop.close()
    return json.dumps(result)
