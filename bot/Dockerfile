FROM python:3.9.5

RUN apt-get update -y
RUN apt-get -y install locales
# Set the locale
RUN sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8

RUN mkdir -p /usr/src/secret_santa

WORKDIR /usr/src/secret_santa

COPY requirements.txt /usr/src/secret_santa
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/secret_santa

CMD python main.py