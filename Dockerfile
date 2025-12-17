# 使用輕量級 Python 3.9
FROM python:3.9-slim

# 安裝必要的系統套件 (Azure Speech SDK 在 Linux 需要 OpenSSL 相關依賴)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    ca-certificates \
    libasound2 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製需求檔並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 開放 Streamlit 預設 Port
EXPOSE 8501

# 設定健康檢查 (Healthcheck) - 選用，但對 Azure 部署有幫助
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 啟動命令
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]