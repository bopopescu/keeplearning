#!/bin/bash
docker run -d -p 8080:80 -v /opt/workplace/nginx/conf.d:/etc/nginx/conf.d -v /opt/workplace/nginx/certs:/etc/nginx/certs -v /var/log/nginx:/var/log/nginx -v /opt/workplace/nginx/www/html:/var/www/html leafsummer/nginx
