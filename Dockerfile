FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip3 install --no-cache-dir -r backend/requirements.txt \
    && pip3 install werkzeug==2.0.3

# 暴露端口
EXPOSE 8000

# 启动Python后端
CMD ["python3", "backend/app.py"]
