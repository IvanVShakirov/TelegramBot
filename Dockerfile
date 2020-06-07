FROM python:3.7

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bot/* ./

# ENV BOT_TOKEN
# ENV ADMIN_ID
# ENV TELEGRAM_PROXY
# ENV DB_NAME
# ENV DB_USER
# ENV DB_PASSWORD
# ENV DB_PORT
# ENV DB_HOST

CMD ["python", "app.py"]
