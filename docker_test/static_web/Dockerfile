# Version: 0.0.1
FROM ubuntu:14.04
MAINTAINER leafsummer "wing.sun1987@gmail.com"
ENV REFRESHED_AT 2016-03-24
RUN apt-get update
RUN apt-get install -y nginx
RUN rm -rf /var/lib/apt/lists/*
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
#RUN echo 'Hello, I am in your container' > /usr/share/nginx/html/index.html

# Define mountable directories.
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx", "/var/www/htwml"]

# Define working directory.
WORKDIR /etc/nginx

# Define default command.
CMD ["nginx"]

EXPOSE 80
EXPOSE 443
