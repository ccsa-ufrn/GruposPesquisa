FROM python:3.5
ADD . /juno
WORKDIR /juno
EXPOSE 3001
RUN pip install -r requirements.txt
