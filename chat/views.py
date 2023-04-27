import json

from django import views
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render

# Magic = ChatGPT assist
from chat import magic, utils
from chat.utils import get_detailed_job_cd_with


def opening_comment(request):
    def content_iterator():
        message = "안녕하세요. 저는 사용자님께 알맞는 취업 정보를 제공해 드릴 김비서 입니다."
        yield f"{message}"

    response = StreamingHttpResponse(content_iterator(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response


class Chat(views.View):
    @staticmethod
    def get(request):
        return render(request, 'chat.html')

    @staticmethod
    def post(request):
        messages = json.loads(request.body)
        response = StreamingHttpResponse(magic.stream_chatting_response(messages), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response


def analyze(messages: list):
    exported_data = magic.convert_chatting_to_info(messages)
    print(exported_data)

    converted_data = magic.convert_info_to_code([{'role': 'user', 'content': exported_data}])
    print(converted_data)

    job_cd = converted_data.split("직무: ")[1].split(",\n")[0]
    job_type = converted_data.split("근무형태: ")[1].split(",\n")[0]
    edu_lv = converted_data.split("학력: ")[1].split(",\n")[0]
    loc_mcd = converted_data.split("지역: ")[1].split("\n")[0]

    exported_job_data = exported_data.split("직무: ")[1].split(",")[0]
    detailed_job_code = magic.convert_job_to_detailed(job_cd, [{'role': 'user', 'content': exported_job_data}])
    print(detailed_job_code)
    extended_job_type = utils.extend_range_of_job_type(job_type)
    print(extended_job_type)
    extended_edu_lvl = utils.extend_range_of_edu_lvl(edu_lv)
    print(extended_edu_lvl)
    print(loc_mcd)

    detailed_job_code = detailed_job_code.replace(' ', '')
    extended_job_type = extended_job_type.replace(' ', '')
    extended_edu_lvl = extended_edu_lvl.replace(' ', '')
    loc_mcd = loc_mcd.replace(' ', '')

    response = utils.job_info_request(detailed_job_code, extended_job_type, extended_edu_lvl, loc_mcd)
    return response['jobs']['job']


class AnalyzeChat(views.View):
    @staticmethod
    def post(request):
        messages = json.loads(request.body)
        job_list = analyze(messages)
        return JsonResponse({'jobs': job_list})
