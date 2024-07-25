FROM python:3.11

# Setup Environment
RUN apt-get update && apt-get upgrade
RUN apt-get install sqlite3

WORKDIR /www

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN mkdir -p var/log

COPY main.py main.py
COPY ./src ./src

ENV mode=production

EXPOSE 80
CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "80"]