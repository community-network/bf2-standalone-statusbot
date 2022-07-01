FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./bot.py bot.py

CMD [ "python", "./bot.py" ]


# use:
# --mount type=bind,source=FOLDERLOCATION_WITH_IMAGES,target=/usr/src/app/maps 