# Use lightweight nginx image
FROM nginx:alpine

# Copy static files
COPY index.html styles.css script.js /app/
COPY health.html /app/

# Create proper nginx config
RUN echo 'server { \
    listen 8080; \
    server_name _; \
    root /app; \
    index index.html; \
    \
    location /health.html { \
        access_log off; \
        add_header Content-Type "text/html; charset=utf-8"; \
        return 200 "OK"; \
    } \
    \
    location / { \
        add_header Cache-Control "no-cache, no-store, must-revalidate"; \
        try_files index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 8080

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
