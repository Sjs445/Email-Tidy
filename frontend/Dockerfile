FROM node:20-alpine as builder

WORKDIR /app
ADD . /app/

RUN npm install

RUN npm run build

FROM nginx
EXPOSE 3000
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/nginx/html
