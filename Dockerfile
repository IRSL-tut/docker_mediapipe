# syntax=docker/dockerfile:1 
FROM ubuntu:22.04

ARG GITHUB_TOKEN
ARG REPOSITORY=IRSL-tut
ARG COMMIT_SHA=master
ENV REPOSITORY ${REPOSITORY}
ENV COMMIT_SHA ${COMMIT_SHA}

# https://qiita.com/haessal/items/0a83fe9fa1ac00ed5ee9
ENV DEBCONF_NOWARNINGS=yes
# https://qiita.com/yagince/items/deba267f789604643bab
ENV DEBIAN_FRONTEND=noninteractive
# https://qiita.com/jacob_327/items/e99ca1cf8167d4c1486d
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

# https://stackoverflow.com/a/25423366
SHELL ["/bin/bash", "-c"]

# https://genzouw.com/entry/2019/09/04/085135/1718/
RUN sed -i 's@archive.ubuntu.com@ftp.jaist.ac.jp/pub/Linux@g' /etc/apt/sources.list

RUN echo 'Asia/Tokyo' > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apt-get update -q -qq && \
    apt-get install -q -qq -y --no-install-recommends tzdata sudo && \
    apt-get install -q -qq -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" keyboard-configuration && \
    apt-get install -q -qq -y sudo build-essential lsb-release wget gnupg2 curl python3-pip && \
    rm -rf /var/lib/apt/lists/*
## aptitude emacs

# Install basic packages
RUN apt-get update -qq && apt-get install -y sudo aptitude build-essential lsb-release wget gnupg2 curl emacs git
RUN aptitude update -q

# vnc
RUN apt-get update && apt-get install -y xvfb x11vnc icewm
RUN echo 'alias vnc="export DISPLAY=:0; Xvfb :0 -screen 0 1400x900x24 &; x11vnc -display :0 -forever -noxdamage > /dev/null 2>&1 &; icewm-session &"' >> /root/.bashrc

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN python3 -m pip install --upgrade pip
RUN pip install --upgrade --user mediapipe

# web camera
RUN apt-get update -qq && apt-get install -y v4l-utils qv4l2