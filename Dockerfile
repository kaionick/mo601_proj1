FROM python:3.10-bullseye

RUN mkdir -p /app
WORKDIR /app

COPY *.py ./

EXPOSE 3000

CMD [ "python3", "circuit_exe.py" ]
