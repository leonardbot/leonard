from sheldon import send_message

def get_answer(message):
    send_message(
        message_text="Тест пройден. Cообщение: '{text}' от {name}".format(
            text=message["message"],
            name=message["name"]
        )
    )
    return True