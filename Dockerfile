FROM ubuntu:latest AS build
RUN apt-get update
RUN apt-get install python3
COPY . .

RUN  pip install -r requirements.txt

FROM python:3.12

EXPOSE 8080

ENTRYPOINT ["streamlit" "run" "CHS_IGBOPE_PORTAL.py" "--server.headless" "true"]
