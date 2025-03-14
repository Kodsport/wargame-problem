FROM node:20

RUN apt-get update && apt-get install -y chromium

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=1
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

WORKDIR /app

COPY . .

RUN useradd --create-home --shell /bin/bash user
RUN chmod -R +rx /app

RUN yarn install --frozen-lockfile && yarn cache clean
RUN yarn build

ENV NODE_ENV=production
ENV BASE_URL="http://localhost:3000"
ENV FLAG="SNHT{seem5_l1ke_y0u_us3d_an_1nter3st1ng_5our53}"

USER user
EXPOSE 3000

CMD ["yarn", "start"]
