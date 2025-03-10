# Price Query System (甲骨文价格查询系统)

## 功能特点

- 实时搜索和过滤
- 价格范围筛选
- 日期范围筛选
- 分页显示
- 响应式设计


## 免责声明

使用本项目（包括但不限于下载、部署、运行）即表示您已充分理解并同意本免责声明的所有条款。

1. 数据相关
   - 本项目展示的数据来源于公开渠道
   - 数据仅供参考，不保证实时性和准确性
   - 使用者应自行验证数据的有效性

2. 使用限制
   - 本项目仅供学习研究使用
   - 不得用于非法用途

3. 风险提示
   - 使用本项目产生的任何直接或间接损失
   - 因数据错误导致的决策失误
   - 因使用不当造成的任何后果

4. 责任限制
   - 作者不对使用后果承担责任
   - 不提供任何形式的保证或担保
   - 使用者需自行承担所有风险

5. 特别说明
   - 本项目不构成任何投资建议
   - 不对因使用本项目导致的任何损失负责
   - 作者保留随时修改或终止服务的权利
  

## 快速开始
### 使用 Docker 运行

```bash
# 拉取镜像
docker pull sparklight233/price-query:v2.0

# 运行容器
docker run -d \
  --name price-query \
  -p 8000:8000 \
  sparklight233/price-query:v2.0
```

## 自定义数据来源


### 1. 获取 excel 文件
1. 找到相关的tg频道，以html格式导出数据
2. 打开导出数据的文件夹，安装依赖，并运行下面的py文件

```
pip install pandas
pip install beautifulsoup4
```


```
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def multi_html_to_excel(html_paths, output_path):
    """同时处理多个HTML文件并合并到单个Excel"""
    data = {
        "地区": [],
        "价格(￥)": [],
        "账号时间(天)": [],
        "出售日期": [],
        "备注": []
    }

    # 处理每个HTML文件
    for html_file in html_paths:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml')

        # 复用之前的解析逻辑
        for message in soup.find_all('div', class_='message'):
            time_div = message.find('div', class_='date')
            if not time_div:
                continue

            # 时间处理增强
            try:
                raw_time = time_div.get('title', '') or time_div.text.strip()
                sell_date = datetime.strptime(raw_time[:10], "%d.%m.%Y").strftime("%Y-%m-%d")
            except Exception as e:
                sell_date = "未知日期"

            # 优化后的正则表达式
            pattern = re.compile(
                r'^([^\d]+?)'          # 地区
                r'(\d+)天\s*'         # 天数
                r'([^￥]*)'           # 规格信息
                r'￥(\d+\.?\d{2})'    # 价格
            )

            for product in message.find_all('a', href=True):
                text = product.text.replace(' ', '')
                if match := pattern.search(text):
                    try:
                        # 数据清洗
                        region = re.sub(r'[^\w\u4e00-\u9fff]', '', match.group(1))
                        days = int(match.group(2))
                        spec = re.sub(r'[-]+', ' ', match.group(3)).strip()
                        price = float(match.group(4))

                        # 存入数据
                        data["地区"].append(region or "未知地区")
                        data["账号时间(天)"].append(days)
                        data["价格(￥)"].append(price)
                        data["出售日期"].append(sell_date)
                        data["备注"].append(spec if spec else None)
                    except Exception as e:
                        continue  # 跳过异常数据

    # 生成合并后的表格
    df = pd.DataFrame(data).drop_duplicates(
        subset=["地区", "账号时间(天)", "价格(￥)", "出售日期"], 
        keep='last'
    ).sort_values(["出售日期", "地区"], ascending=[False, True])

    # 保存结果
    try:
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"成功合并 {len(html_paths)} 个文件，共 {len(df)} 条记录")
    except Exception as e:
        print(f"保存失败：{str(e)}")

# 使用示例
multi_html_to_excel(
    html_paths=['messages.html', 'messages2.html'], 
    output_path='data.xlsx'
)
```

### 2. 上传数据文件
上传数据文件到/path/to/your/data，文件为之前获取的excel文件

```
mkdir -p /path/to/your/data
```

### 3. 运行容器
```
# 拉取镜像
docker pull sparklight233/price-query:v2.0

# 运行容器
docker run -d \
  --name price-query \
  -p 8000:8000 \
  -v /data/price-query:/app/data \
  sparklight233/price-query:v2.0
```


### 数据来源

雷总的[频道](https://t.me/masta_ee)

### 本地编译

```
# 拉取源码
git clone https://github.com/sparklight233/price-query.git

# 安装Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
apt-get install -y nodejs

# 确认安装
node -v
npm -v

# 构建前端
cd ~/project/price-query/frontend
npm install
npm run build

# 构建docker
cd ..
docker build -t sparklight233/price-query:v2.0 .
docker push sparklight233/price-query:v2.0
```
