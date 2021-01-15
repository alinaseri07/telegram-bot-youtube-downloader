FROM python:3.8

WORKDIR /app

COPY main.py .
COPY .env .

# install dependencies
RUN pip3 install telebot
RUN pip3 install pytube
RUN pip3 install pyTelegramBotAPI
RUN pip3 install python-dotenv

# command to run on container start
CMD [ "python", "./main.py" ]