FROM registry.access.redhat.com/ubi10/nginx-126:latest

LABEL org.opencontainers.image.source="https://github.com"

USER root

COPY dist /usr/share/nginx/html

USER 1001

ENTRYPOINT ["nginx", "-g", "daemon off;"]