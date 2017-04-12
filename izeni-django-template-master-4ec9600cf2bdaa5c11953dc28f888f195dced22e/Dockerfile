FROM python:3.5

ENV CPATH=/usr/local/include/python3.5m

RUN apt-get --quiet -y update && apt-get install --quiet -y wget \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /
RUN pip install django
RUN bash -c "bash <(wget -qO- https://dev.izeni.net/izeni/izeni-django-template/raw/master/startproject.sh) izeni_django"

WORKDIR /izeni_django

RUN pip install --no-cache-dir --src /usr/src -r requirements.txt

CMD ["/bin/bash"]
