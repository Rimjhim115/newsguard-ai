# frontend/Dockerfile
# PURPOSE: Build a container for the React frontend.
#
# We use a two-stage build:
# Stage 1 (builder): Install dependencies and build React app
# Stage 2 (production): Serve the built files with nginx
#
# This keeps the final image small — we don't need Node.js
# in production, just the built HTML/CSS/JS files.

# Stage 1 — Build
FROM node:20-slim AS builder

WORKDIR /app

# Copy package files first (layer caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the React app for production
RUN npm run build

# Stage 2 — Serve with nginx
FROM nginx:alpine

# Copy built files from Stage 1
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]