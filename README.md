# Docker Image Creation and Vulnerability Auditing

This document outlines the steps to create three different Docker images and audit them for vulnerabilities using Docker Scout.

## 1. Image with `curl`

This image installs `curl` and executes `curl google.com` upon running.

**Build the image:**
```bash
docker build -t curl-image -f Dockerfile.curl .
```

**Run the container:**
```bash
docker run --rm curl-image
```

## 2. Image Serving Static HTML

This image uses Nginx to serve a simple static HTML page.

**Build the image:**
```bash
docker build -t static-html-image -f Dockerfile.nginx .
```

**Run the container:**
```bash
# Runs in detached mode, maps host port 8080 to container port 80
docker run --rm -d -p 8080:80 static-html-image
```
*Access the page at `http://localhost:8080` in your browser.*

## 3. Image with a Basic Python Web Server

This image runs a simple web server written in Python using the built-in `http.server` module.

**Build the image:**
```bash
# Create the dummy web/index.html first by running server.py locally once
# or manually create the web directory and an index.html file inside it.
# Then build:
docker build -t python-server -f Dockerfile.python .
```

**Run the container:**
```bash
# Runs in detached mode, maps host port 8001 to container port 8000
docker run --rm -d -p 8001:8000 python-server
```
*Access the server at `http://localhost:8001` in your browser.*

## 4. Auditing Vulnerabilities with Docker Scout

Docker Scout helps identify Common Vulnerabilities and Exposures (CVEs) in your Docker images.

**Prerequisites:**
*   Docker Desktop with Docker Scout enabled or Docker Engine with the `docker scout` CLI plugin installed.
*   Log in to Docker Hub (`docker login`). Docker Scout might require a Docker Pro, Team, or Business subscription for advanced features or frequent use, but basic CVE scanning is often available.

**Audit an image (e.g., the Python server image):**
```bash
# Ensure the image is built, e.g., python-server
docker scout cves python-server
```

**Interpreting Results:**
Docker Scout will list vulnerabilities found in the image layers, often categorized by severity (Critical, High, Medium, Low). It shows the vulnerable package, version, and the fixed version if available.

**Addressing Vulnerabilities (Example: `python-server`):**

1.  **Run the audit:** `docker scout cves python-server`
2.  **Analyze:** Look for vulnerabilities, especially High and Critical ones. Note the affected packages (e.g., `openssl`, `python`, base OS packages).
3.  **Update Base Image:** The easiest fix is often using the *latest patch version* of your chosen base image tag (e.g., `python:3.11.x-slim` instead of just `python:3.11-slim`, although `slim` tags are usually updated). Check Docker Hub for the latest available tags. Modify the `FROM` line in `Dockerfile.python`.
4.  **Update OS Packages:** If vulnerabilities persist in OS packages, add commands to update them *after* the `FROM` line and *before* copying application code.
    ```dockerfile
    FROM python:3.11-slim
    # Update packages (example for Debian/Ubuntu based slim images)
    RUN apt-get update && apt-get upgrade -y --no-install-recommends && rm -rf /var/lib/apt/lists/*
    WORKDIR /app
    # ... rest of Dockerfile
    ```
5.  **Rebuild:** `docker build -t python-server -f Dockerfile.python .`
6.  **Re-audit:** `docker scout cves python-server`. Compare results.
7.  **Consider Multi-stage Builds:** For production applications, use multi-stage builds. One stage builds the app (including dev dependencies), and a final *minimal* stage copies only the necessary runtime files and dependencies, significantly reducing the attack surface.

By iteratively updating base images and packages, you can reduce the number of known vulnerabilities reported by Docker Scout.