FROM python:3.5

ENV CPATH=/usr/local/include/python3.5m

RUN mkdir /{{ project_name }}
WORKDIR /{{ project_name }}

ADD requirements.txt /{{ project_name }}/requirements.txt
RUN pip install --no-cache-dir --src /usr/src -r requirements.txt

ADD . /{{ project_name }}
