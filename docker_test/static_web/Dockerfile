# Version: 0.0.1
FROM ubuntu:14.04
MAINTAINER leafsummer "wing.sun1987@gmail.com"
ENV REFRESHED_AT 2016-03-24
RUN apt-get update
RUN apt-get install -y nginx
RUN echo 'Hello, I am in your container' > /usr/share/nginx/html/index.html
EXPOSE 80
