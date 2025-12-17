# 使用 Python 3.9 Slim 版
FROM python:3.9-slim

# 安裝必要的系統相依套件 (Azure Speech SDK 需要)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    ca-certificates \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 複製並安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 開放容器內部的 8501 Port (Streamlit 預設)
EXPOSE 8501

# 設定啟動指令
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]