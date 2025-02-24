FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用文件
COPY app /app/

# 列出文件以验证
RUN ls -la /app && \
    ls -la /app/static && \
    ls -la /app/templates

EXPOSE 8000

CMD ["python", "app.py"]
