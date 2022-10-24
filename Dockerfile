FROM python:3.9-alpine
LABEL MAINTAINER="coccoinomane <coccoinomane@gmail.com>"
ENV PS1="\[\e[0;33m\]|> web3cli <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "

WORKDIR /src
COPY . /src
RUN pip install pdm
RUN pdm install
WORKDIR /
ENTRYPOINT ["web3cli"]
