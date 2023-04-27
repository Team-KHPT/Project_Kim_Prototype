import openai

from chat.utils import get_detailed_job_cd_with


def get_prompts(job_cd: int) -> list:
    prompts = [
        {
            'role': 'system',
            'content': f'''Based on the below table, pick one or more codes that is related to keyword.
If you picked multiple codes, please separate them with commas.
If you can't answer, say error.

Table
{get_detailed_job_cd_with(job_cd)}
'''
         },
        {'role': 'user', 'content': '''백엔드 개발자'''},
        {'role': 'assistant', 'content': '''84'''},
        {'role': 'user', 'content': '''Unity 게임 개발자'''},
        {'role': 'assistant', 'content': '''80,304'''},
        {'role': 'user', 'content': '''ㄹㄷㅈㄹㄷㄹㅈㄷ'''},
        {'role': 'assistant', 'content': '''error'''},
        {'role': 'user', 'content': '''dsff'''},
        {'role': 'assistant', 'content': '''error'''},
    ]
    return prompts


def convert_job_to_detailed(job_cd: str, messages: list) -> str:
    if not job_cd.isdigit():
        return ''
    else:
        job_cd = int(job_cd)
    print(get_prompts(job_cd))
    if len(get_detailed_job_cd_with(job_cd)) < 1:
        return ''
    messages[:0] = get_prompts(job_cd)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=128,
        temperature=0.4,
        messages=messages
    )
    return completion['choices'][0]['message']['content']
