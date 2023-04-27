import os

import pandas as pd
from django.conf import settings


def get_loc_mcd_data() -> str:
    filename = os.path.join(settings.BASE_DIR, 'chat', 'code_tables', 'loc_mcd.csv')
    df = pd.read_csv(filename)
    return df.to_string(index=False)


def get_job_type_data() -> str:
    filename = os.path.join(settings.BASE_DIR, 'chat', 'code_tables', 'job_type.csv')
    df = pd.read_csv(filename)
    return df.to_string(index=False)


def get_edu_lvl_data() -> str:
    filename = os.path.join(settings.BASE_DIR, 'chat', 'code_tables', 'edu_lvl.csv')
    df = pd.read_csv(filename)
    return df.to_string(index=False)


def get_job_cd_data() -> str:
    filename = os.path.join(settings.BASE_DIR, 'chat', 'code_tables', 'job_cd.csv')
    df = pd.read_csv(filename)
    return df.to_string(index=False)


def get_detailed_job_cd_with(job_cd: int) -> str:
    filename = os.path.join(settings.BASE_DIR, 'chat', 'code_tables', 'job_cd_detailed.csv')
    df = pd.read_csv(filename)
    narrowed_data = df[df['job_mid_cd'] == job_cd]
    narrowed_data = narrowed_data.drop('job_mid_cd', axis=1)
    csv_str = narrowed_data.to_csv(index=False)
    return csv_str
