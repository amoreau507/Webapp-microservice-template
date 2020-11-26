# All credits goes to  https://vuejs.org/v2/cookbook/dockerize-vuejs-app.html
FROM node:lts-alpine

RUN npm install -g http-server

RUN apk add --no-cache openssl

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build
RUN openssl req -new -newkey rsa:2048 -days 3650 -nodes -x509 -subj "/C=CA/ST=QC/L=MTL/O=Patate/CN=auFour" -keyout key.pem -out cert.pem

EXPOSE 8181
CMD [ "http-server", "dist","-S","-p","8181"]