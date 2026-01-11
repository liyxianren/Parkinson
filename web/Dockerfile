
# Stage 1: Build Frontend
FROM node:18-alpine as frontend-builder

WORKDIR /app/frontend

# Copy frontend dependency files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ .

# Build frontend
RUN npm run build

# Stage 2: Build Backend & Final Image
FROM python:3.10-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

# Copy built frontend assets from Stage 1 to backend's static directory
# app/main.py expects static files in ../static relative to app/
COPY --from=frontend-builder /app/frontend/dist /app/static

# Expose the port
EXPOSE 8000

# Start command (using shell form to expand PORT variable)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
