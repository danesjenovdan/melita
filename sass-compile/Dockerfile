# ---------------------------------- WARNING ----------------------------------
# This file is primarily for development use with docker-compose
# See Dockerfile in repository root for production and k8s use
# ---------------------------------- WARNING ----------------------------------

FROM node:18-alpine

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn

CMD yarn css
