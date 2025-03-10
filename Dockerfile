FROM node:16

# 设置工作目录
WORKDIR /app

# 安装Python和pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装Node.js依赖并构建前端
WORKDIR /app/frontend
RUN npm install && npm run build

# 回到主工作目录
WORKDIR /app

# 安装Python依赖
RUN pip3 install --no-cache-dir -r backend/requirements.txt

# 暴露端口
EXPOSE 3000

# 启动Python后端
CMD ["python3", "backend/app.py"]