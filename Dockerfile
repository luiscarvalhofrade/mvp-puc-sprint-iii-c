# syntax=docker/dockerfile:1
FROM python:3.11.5-slim
WORKDIR /mvp-puc-sprint-iii-c
COPY . /mvp-puc-sprint-iii-c
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5010
CMD ["flask", "--app" , "service", "run", "--host=0.0.0.0", "--port=5011"]