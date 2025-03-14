FROM node:20-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache sqlite

WORKDIR /app

COPY . .

RUN npm i

ENV FLAG=SNHT{i_love_banananananananananananananananas}

EXPOSE 3000

CMD ["node", "main.js"]