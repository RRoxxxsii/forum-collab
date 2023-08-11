# Install dependencies only when needed
FROM node:18-alpine

WORKDIR /next

# Install dependencies based on the preferred package manager
COPY package*.json ./

COPY . .

# Exposing the Application Port
EXPOSE 3000

RUN npm install

RUN npm start