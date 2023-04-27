import openai
from django.conf import settings

openai.api_key = settings.OPENAI_KEY

prompt = {
    'role': 'user',
    'content': '''지금까지 알아낸 정보를 아래와 같은 형식으로 말해줘. 모르는 값은 none 이라고 해줘.

info: [
직무: {직무},
근무형태: {근무형태},
학력: {학력},
지역: {지역}
]'''
}


def convert_chatting_to_info(messages: list):
    messages.append(prompt)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=128,
        temperature=0.4,
        messages=messages
    )
    return completion['choices'][0]['message']['content']
