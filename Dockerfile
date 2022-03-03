FROM python:3.9-buster

# Locale 설정
ENV LANG ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

# stop Python from generating .pyc files, and enable Python tracebacks on segfaults:
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

# 해당 디렉토리로 이동
WORKDIR /usr/src/app

COPY . .

# 의존성 설치
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install  --deploy --system
