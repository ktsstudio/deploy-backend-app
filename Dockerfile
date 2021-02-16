FROM python:3.9
# gettext-base нужен для того, чтобы установить envsubst
RUN apt update && apt -y install gettext-base
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# подставляем переменные из окружения в подготовленный конфиг
CMD ["./run.sh"]
