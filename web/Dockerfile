FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d

WORKDIR /static
COPY ./static /static

WORKDIR /media
COPY ./media /media

WORKDIR /docs
COPY ./docs /docs