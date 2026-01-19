# 当当网图书爬虫（Scrapy 项目）

一个基于 Scrapy 的当当网图书信息爬虫，支持按分类自动抓取书籍数据，并生成多个分类独立的 CSV 文件。

## 项目功能

- 从当当网“图书”大类下自动获取所有子分类
- 支持多页翻页爬取
- 提取字段：分类、书名、作者、价格、出版社、商家、简介
- 自动清洗数据（去掉价格中的 ¥ 符号、处理空值默认显示）
- 按分类保存为独立的 CSV 文件（存放在 `output/` 文件夹）
- 文件名自动添加时间戳，避免多次运行覆盖
- 简单去重（书名 + 作者 + 出版社 作为唯一标识）
- 包含基本防反爬设置（延时、User-Agent）

## 技术栈

- Python 3.8+
- Scrapy
- csv（标准库）
- itemadapter
- requests
- time
- 

## 目录结构
scrapy_DD/
├── scrapy.cfg
├── scrapy_DD/
│   ├── init.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py          # 核心：按分类保存 CSV + 去重
│   ├── settings.py
│   └── spiders/
│       └── DDbook.py         # 主爬虫文件
├── output/                   # 运行后自动生成，按分类 + 时间戳保存的 CSV
└── README.md
text## 安装与运行

### 1. 克隆仓库

```bash
git clone https://github.com/demanlover9/scrapy-dangdang-books.git
cd scrapy-dangdang-books
2. 创建虚拟环境 & 安装依赖
Bash# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
Bashpip install scrapy
3. 运行爬虫
Bashscrapy crawl DDbook
爬取完成后，数据会自动保存在 output/ 文件夹中，每个分类一个带时间戳的 CSV 文件，例如：
textoutput/青春文学_20260119_061234.csv
output/现代言情_20260119_061234.csv
...
配置建议（settings.py）
Python# 防反爬（强烈建议开启）
DOWNLOAD_DELAY = 2.0
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# 启用 pipeline
ITEM_PIPELINES = {
    'scrapy_DD.pipelines.ScrapyDdPipeline': 300,
}

# 日志级别（方便观察）
LOG_LEVEL = 'INFO'

后续可能改进的方向

 支持更多字段（ISBN、评分、评论数、出版时间等）
 增加随机 User-Agent 池
 支持代理 IP 池
 导出为 Excel (.xlsx) 格式
 添加命令行参数（指定关键词、分类、页数范围等）
