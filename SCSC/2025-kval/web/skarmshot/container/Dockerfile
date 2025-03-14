FROM node:20

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true

RUN apt-get update && apt-get install curl gnupg -y \
    && curl --location --silent https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable gcc xxd \
    && rm -rf /var/lib/apt/lists/*

ENV XDG_CONFIG_HOME=/tmp/.chromium
ENV XDG_CACHE_HOME=/tmp/.chromium

WORKDIR /app

COPY . .

RUN useradd user
RUN chmod -R  +rx /app
RUN chmod 400 flag.txt

RUN gcc readflag.c -o readflag
RUN chmod u+s readflag

RUN admin_token=$(head -c 32 /dev/urandom | xxd -p -c 32) && \
    echo "module.exports = {admin_token:\"$admin_token\"};" > config.js

RUN npm i

USER user

EXPOSE 3000

CMD ["node", "--inspect", "index.js"]