FROM nginx:1.25.4-alpine3.18

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d

WORKDIR /static
COPY ./static /static

WORKDIR /media
COPY ./media /media

WORKDIR /docs
COPY ./docs /docs