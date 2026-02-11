# Use lightweight nginx image
FROM nginx:alpine

# Copy static files
COPY index.html styles.css script.js /app/
COPY health.html /app/

# Add nginx config
RUN echo 'server { \
    listen 8080; \
    server_name _; \
    \
    location / { \
        root /app; \
        try_files index.html; \
        add_header Cache-Control "no-cache"; \
        \
        location = /health.html { \
            access_log off; \
            return 200 "OK"; \
        } \
    } \
}' > /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
