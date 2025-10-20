FROM node:20-alpine

WORKDIR /web

COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN npm install

COPY . .

ENV VITE_API_BASE_URL=http://api:8000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
