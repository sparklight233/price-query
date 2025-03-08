from flask import Flask, render_template, jsonify
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

app = Flask(__name__)

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
        df['价格(￥)'] = pd.to_numeric(df['价格(￥)'], errors='coerce').fillna(0)
        df['账号时间(天)'] = pd.to_numeric(df['账号时间(天)'], errors='coerce').fillna(0).astype(int)
        
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
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    logger.info("应用启动中...")
    app.run(host='0.0.0.0', port=8000)
