FROM python:slim AS app

WORKDIR /app

RUN pip install --no-cache-dir pycryptodome Flask

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]