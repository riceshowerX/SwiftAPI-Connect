
# SwiftAPI-Connect

SwiftAPI-Connect 是一个基于 FastAPI 的强大 API 连接器，用于模拟 HTTP 请求并提供用户界面进行测试。

## 目录结构

```
SwiftAPI-Connect/
├── run.py                 # 主运行脚本
├── fastapi_server.py      # FastAPI 服务器配置
├── app/
│   ├── __init__.py        # 初始化模块
│   ├── main.py            # 主应用入口
│   ├── routers/           # 路由模块
│   │   ├── __init__.py    # 初始化路由模块
│   │   ├── http_mock.py   # HTTP Mock 路由
│   ├── utils/             # 工具模块
│   │   ├── __init__.py    # 初始化工具模块
│   │   ├── request_helper.py # 请求辅助工具
│   │   ├── encoding_helper.py # 编码辅助工具
│   ├── schemas/           # 模式定义模块
│   │   ├── __init__.py    # 初始化模式模块
│   │   ├── request_schema.py  # 请求模式定义
│   │   ├── response_schema.py # 响应模式定义
├── ui/
│   └── app.py             # UI 应用入口
└── requirements.txt       # 依赖包列表
```

## 使用说明

1. **克隆项目到本地：**

    ```bash
    git clone https://github.com/your_username/SwiftAPI-Connect.git
    ```

2. **安装依赖：**

    ```bash
    cd SwiftAPI-Connect
    pip install -r requirements.txt
    ```

3. **运行应用程序：**

    ```bash
    streamlit run ui/app.py
    ```

4. **访问用户界面：**

    打开浏览器并访问 [http://localhost:8501](http://localhost:8501)。

## 贡献

欢迎贡献代码，提出建议或报告问题。您可以通过提交 pull request 或 issue 来贡献。

## 许可证

本项目采用 Apache License 2.0 许可证。详细信息请参阅 [LICENSE](LICENSE) 文件。