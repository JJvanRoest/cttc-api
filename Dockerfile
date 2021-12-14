FROM alpine:3.14

# make sure TZ is not set as env variable, that breaks the timezone setup, when you set TZ it required the tzdata package at runtime
ARG TZ=Europe/Amsterdam
ENV MYSQL_CHARSET utf8mb4

# instead of setting WORKDIR we create the app directory first to copy stuff in before calling WORKDIR because of editable packages
# see: https://stackoverflow.com/questions/29905909/pip-install-e-packages-dont-appear-in-docker
RUN mkdir -p /usr/src/app

# install python3 from apk repo and remove unnecessary stuff afterwards
# from https://hub.docker.com/r/joshuarli/alpine-python3-pip/
# install openssl to support https
# install git to clone Python packages from git repos
# upgrade pip to support more dependencies
RUN apk add --update --no-cache python3 libuuid \
    py3-pip \
    ca-certificates \
    git \
    openssh-client \
    libpng \
    libstdc++ \
    openssl \
    musl && \
    find / -type d -name __pycache__ -exec rm -r {} +   && \
    rm -r /usr/lib/python*/ensurepip                    && \
    rm -r /usr/lib/python*/lib2to3                      && \
    rm -r /usr/lib/python*/turtledemo                   && \
    rm /usr/lib/python*/turtle.py                       && \
    rm /usr/lib/python*/webbrowser.py                   && \
    rm /usr/lib/python*/doctest.py                      && \
    rm -rf /root/.cache /var/cache /usr/share/terminfo  && \
    pip3 install --upgrade pip==21.2.4

# install build dependencies, use those to build the python dependencies (pip install) and then remove the build dependencies
# doing this in one RUN command ensures that the build dependencies are not added to a layer of the docker image
# --update means update the sources before installing (instead of doing apk update and then apk add)
# --no-cache means don't save cache to the disk/docker image (smaller docker image)
# --virtual is to easily delete all the build dependencies afterwards
COPY requirements.txt /usr/src/app
RUN mkdir -p /var/cache/apk \
    && apk add --update --no-cache --virtual .build-deps \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    py3-wheel \
    freetype-dev \
    linux-headers \
    bsd-compat-headers \
    tzdata \
    cargo \
    postgresql-dev \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && pip install wheel \
    && pip --no-cache-dir install -r /usr/src/app/requirements.txt --ignore-installed \
    && apk --no-cache del .build-deps \
    && rm -r /var/cache

ENV PYTHONUNBUFFERED=1

# copy the source code to the image
COPY . /usr/src/app

WORKDIR /usr/src/app

# this only signals that there runs a service on port 8000, funtionally this does not really do anything.
EXPOSE 8000

# default action is to run the production server
# see docker-compose.yml for the command to run the dev server (default if you start it with docker-compose)
ENTRYPOINT ["hypercorn", "app:app", "-c", "config.toml"]
