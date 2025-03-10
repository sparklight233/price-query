from flask import Flask, render_template, jsonify, send_from_directory
import pandas as pd
import os
import logging
import glob

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 在app初始化之前添加
data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(data_dir, exist_ok=True)

app = Flask(__name__, 
            static_folder='../dist',
            static_url_path='')

def load_data():
    try:
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        excel_files = glob.glob(os.path.join(data_dir, '*.xlsx'))
        
        if not excel_files:
            logger.error(f"未在 {data_dir} 目录下找到Excel文件")
            return []
            
        excel_file = excel_files[0]
        logger.info(f"正在读取文件: {excel_file}")
        
        # 读取Excel文件
        df = pd.read_excel(excel_file)
        
        # 确保列名正确
        expected_columns = ['地区', '价格(￥)', '账号时间(天)', '出售日期', '备注']
        if list(df.columns) != expected_columns:
            logger.warning(f"列名不匹配。期望: {expected_columns}, 实际: {list(df.columns)}")
            # 重命名列
            df.columns = expected_columns
        
        # 处理数据类型
        df = df.fillna('')
        # 修复价格列的处理方式
        df['价格(￥)'] = pd.to_numeric(df['价格(￥)'], errors='coerce')
        df['价格(￥)'] = df['价格(￥)'].replace(pd.NA, 0).astype(float)
        df['账号时间(天)'] = pd.to_numeric(df['账号时间(天)'], errors='coerce')
        df['账号时间(天)'] = df['账号时间(天)'].replace(pd.NA, 0).astype(int)
        
        # 重命名列以匹配前端期望的格式
        df = df.rename(columns={
            '价格(￥)': '价格',
            '账号时间(天)': '账号时间'
        })
        
        # 转换为字典
        data = df.to_dict('records')
        logger.info(f"成功加载 {len(data)} 条记录")
        
        # 打印前几条记录用于调试
        logger.info(f"数据示例: {data[:2]}")
        
        return data
        
    except Exception as e:
        logger.error(f"加载数据错误: {str(e)}")
        logger.exception("详细错误信息：")
        return []

@app.route('/')
def index():
    # 使用send_static_file而不是render_template
    return app.send_static_file('index.html')

# 添加处理前端路由的函数
@app.route('/<path:path>')
def serve_static(path):
    try:
        # 确保path不为None
        if path is None:
            logger.warning("路径为None，返回index.html")
            return app.send_static_file('index.html')
            
        # 确保static_folder不为None
        static_folder = app.static_folder or ''
        
        static_path = os.path.join(static_folder, path)
        if os.path.exists(static_path) and os.path.isfile(static_path):
            return send_from_directory(static_folder, path)
        else:
            logger.info(f"路径不存在或不是文件，返回index.html: {path}")
            return app.send_static_file('index.html')
    except Exception as e:
        logger.error(f"提供静态文件时出错: {str(e)}")
        return app.send_static_file('index.html')

@app.route('/api/data')
def get_data():
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    logger.info("应用启动中...")
    app.run(host='0.0.0.0', port=8000)
