# Version: 0.0.1
FROM ubuntu:14.04
MAINTAINER leafsummer "wing.sun1987@gmail.com"
ENV REFRESHED_AT 2016-03-24
RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
RUN echo "deb http://nginx.org/packages/mainline/ubuntu/ trusty nginx" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y ca-certificates nginx gettext-base 
RUN rm -rf /var/lib/apt/lists/*
#RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
#RUN echo 'Hello, I am in your container' > /usr/share/nginx/html/index.html
RUN rm -rf /etc/nginx/conf.d/*.*
RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /var/www/html
RUN chown -R root:www-data /var/www/html
RUN chmod -R 755 /var/www/html
COPY vhost.conf /etc/nginx/sites-enabled/vhost.conf
COPY index.html /var/www/html/index.html
RUN chmod 755 /var/www/html/index.html
# Define mountable directories.
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx", "/var/www/html"]

# Define working directory.
WORKDIR /etc/nginx

# Define default command.
CMD ["nginx"]

EXPOSE 80
EXPOSE 443
