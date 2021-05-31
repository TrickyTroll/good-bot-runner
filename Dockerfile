FROM python:3.9

WORKDIR /app

COPY . .

RUN pip3 install .

CMD ["runner", "./samples/passwords.yaml"]
