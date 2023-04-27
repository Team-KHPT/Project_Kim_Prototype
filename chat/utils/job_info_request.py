import json

import requests
from django.conf import settings


def job_info_request(ind_cd, job_type, edu_lv, loc_mcd) -> dict:
    url = "https://oapi.saramin.co.kr/job-search"
    params = {
        "job_cd": ind_cd,
        "job_type": job_type,
        "edu_lv": edu_lv,
        "loc_mcd": loc_mcd,
        "count": "20",
        "access-key": settings.SARAMIN_KEY
    }

    response = requests.get(url, params=params)
    print(response.url)
    print(response.headers)
    jobs = json.loads(response.text)
    return jobs
