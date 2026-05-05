FROM python:3.11-slim

# Install Chromium properly
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Yeh ensure karega ki Chromium sahi version hai
RUN chromium --version && chromedriver --version

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8505

# --headless mode container ke liye
ENV DISPLAY=:99

CMD streamlit run app.py --server.port=8080 --server.address=0.0.0.0
