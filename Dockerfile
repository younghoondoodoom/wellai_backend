#python 3.10-alpine 버전을 사용하겠다
FROM python:3.10-alpine

# Locale 설정
ENV LANG ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

# stop Python from generating .pyc files, and enable Python tracebacks on segfaults:
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

# postgresql
# RUN apk update \
#     && apk install -y --no-install-recommends \
#     postgresql-client \
#     && rm -rf /var/lib/apt/lists/*


# psycopg2 의존성 추가
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add libffi-dev

# pipenv 설치
# RUN pip install pipenv
# RUN pipenv install --system --deploy

# 해당 디렉토리로 이동
WORKDIR /usr/src/app

# 현재 경로, Dockerfile이 위치한 경로에 있는 모든 파일을 지금 위치로 복사해 온다
COPY . .

# 장고 웹서버 8000 포트를 컨테이너에서도 열어줌
EXPOSE 8000

# 의존성 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 장고 실행 명령어
RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh","./entrypoint.sh"]
# CMD ["./entrypoint.sh"]
# CMD ["python3", "manage.py", "runserver", "0:8000"]
# CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]



# RUN pipenv install gunicorn