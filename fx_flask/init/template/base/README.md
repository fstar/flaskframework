```commandline
.
├── app
│   ├── adapter       # 数据转换器, 例如在医院里对接外部系统的时候, 需要将 entity 里的数据转化成对方的数据结构 
│   ├── constants     # 常量
│   ├── entity        # 实例的数据格式定义, 通常里面都是一些 dataclass
│   ├── exceptions    # 自定义异常
│   ├── platform      # 与平台通信的 client
│   ├── repository    # 数据交互层, 主要是数据存取的封装, 作用是为了屏蔽掉数据来源, 例如目前数据存储在磁盘中, 将来如果用云存储, 只要改这一层的实现即可; 也可以做数据加解密操作。
│   ├── resources     # 接口层
│   ├── schemas       # 接口数据格式定义, 通常里面都是一些 dataclass
│   ├── services      # 业务层
│   ├── tasks         # 异步任务, 例如目前的 celery worker 操作
│   ├── utils         # 工具包, 存放一些通用函数
│   ├── validator     # 校验器, 例如校验后管配置是否合法
│   ├── ./celery_app.py      # celery app 初始化
│   ├── ./dependencies.py    # 初始化配置
│   ├── ./flask_app.py       # 初始化 flask app
│   ├── ./flask_restx_api.py # 初始化 flask-restx app
│   └── ./translations.py    # 翻译功能
├── build          # 存放 dockerfile 
├── configs        # 配置项
├── doc            # 文档
├── logs           # 日志
├── migrations     # migrations
├── sample_data    # 样例数据
├── tests          # 单元测试
├── translations   # 国际化翻译
├── ./CHANGELOG    # 版本更新日志
├── ./README.md    # 说明文档
├── ./VERSION      # 版本信息
├── ./manage.py    # 程序启动入口
├── ./requirements-dev.txt  # 本地开发用的依赖包
└── ./requirements.txt      # 线上环境依赖包
```
## 安装依赖
pip install -r requirements.txt

## 初始化步骤
python manage.py run-init-data

## 启动 flask api 服务
python manage.py run-api-server

## 启动 监听dispatch 服务
python manage.py run-do-postprocess-consumer

## 启动 监听alg状态消息 服务
python manage.py run-alg-consumer

## 启动轮询任务
python manage.py run-scheduler

## 生成 docker 镜像
docker build -f ./build/dockerfile -t <image_name>:<image_tag> .