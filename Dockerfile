FROM python:3.11

WORKDIR /www

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY main.py main.py
COPY ./src ./src

CMD ["fastapi", "run", "app/main.py", "--port", "80"]