import openai

from chat.utils import get_job_type_data, get_loc_mcd_data, get_job_cd_data, get_edu_lvl_data


prompts = [
    {'role': 'system', 'content': f'''아래의 테이블을 참고해서 하나 이상의 코드로 바꿔줘. 해당하는 코드가 없다면 비슷한 것을 골라서 코드로 바꿔줘.

코드만 답변해줘.
none은 -1 이라고 출력해줘.

근무 형태 테이블.
{get_job_type_data()}

지역 테이블.
{get_loc_mcd_data()}

직무 테이블.
{get_job_cd_data()}

학력 테이블.
{get_edu_lvl_data()}
'''
     },
    {'role': 'user', 'content': '''info: [직무: 유치원교사]'''},
    {'role': 'assistant', 'content': '''info: [직무: 19]'''},
    {'role': 'user', 'content': '''info: [
    직무: IT,
    근무형태: 안정적인 형태,
    학력: 고등학교 졸업 예정,
    지역: none
    ]'''
     },
    {'role': 'assistant', 'content': '''직무: 2,
    근무형태: 1,
    학력: 1,
    지역: -1'''
     }
]


def convert_info_to_code(messages: list) -> str:
    print(prompts)
    messages[:0] = prompts
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=128,
        temperature=0.4,
        messages=messages
    )
    return completion['choices'][0]['message']['content']
