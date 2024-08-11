FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY --from=build /app/package*.json ./
RUN npm install --only=production
RUN npm install pm2 -g

COPY --from=build /app/dist ./dist

USER node

ENV PORT=4000
EXPOSE 4000

CMD ["pm2-runtime", "dist/main.js"]
