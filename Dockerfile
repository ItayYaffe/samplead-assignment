FROM postgres:16-alpine

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=samplead

COPY ./schema.sql/ /docker-entrypoint-initdb.d/

EXPOSE 5432
