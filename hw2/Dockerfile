FROM debian:buster-slim

RUN apt-get update && apt-get install -y python3 iputils-ping

WORKDIR /find_mtu

COPY . .
