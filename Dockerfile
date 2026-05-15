# Use lightweight nginx image
FROM nginx:alpine

# Copy static files
COPY index.html styles.css script.js robots.txt sitemap.xml /app/
COPY health.html /app/
COPY resume.txt resume.json llms.txt /app/
COPY docs /app/docs

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
    location = /resume.txt { \
        add_header Content-Type "text/plain; charset=utf-8"; \
        add_header X-Robots-Tag "all"; \
        add_header Cache-Control "public, max-age=3600"; \
        try_files $uri =404; \
    } \
    \
    location = /resume.json { \
        add_header Content-Type "application/json; charset=utf-8"; \
        add_header Access-Control-Allow-Origin "*"; \
        add_header X-Robots-Tag "all"; \
        add_header Cache-Control "public, max-age=3600"; \
        try_files $uri =404; \
    } \
    \
    location = /llms.txt { \
        add_header Content-Type "text/markdown; charset=utf-8"; \
        add_header X-Robots-Tag "all"; \
        add_header Cache-Control "public, max-age=3600"; \
        try_files $uri =404; \
    } \
    \
    location ~* \.pdf$ { \
        add_header Content-Type "application/pdf"; \
        add_header Content-Disposition "attachment"; \
        try_files $uri =404; \
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
