# SwiftAPI-Connect

SwiftAPI-Connect 是一个基于 FastAPI 的强大 API 连接器，旨在模拟 HTTP 请求并为测试提供用户界面。该项目的主要目标是简化开发人员的测试过程，并提供一种直观的方式来检查和验证 API 的行为。

**免责声明：** 本项目按原样提供，不附带任何明示或暗示的保证。使用者需自行承担风险。本项目的作者和贡献者对因使用本软件而导致的任何损失或损害不承担任何责任。

## 主要特性

- **使用 FastAPI 构建**，提供快速和高效的 API 服务。
- **内置用户界面**，可视化展示 HTTP 请求和响应，并提供简单易用的操作界面。
- **支持模拟 HTTP 请求**，包括 GET、POST、PUT、DELETE 等各种方法。
- **提供详细的响应信息**，便于检查和调试 API 响应。
- **支持 API 密钥验证**，确保 API 的安全性。
- **支持自动检测响应内容编码**，并进行解码。
- **提供响应时间图表**，方便分析请求性能。
- **支持自定义数据格式**，方便处理不同类型的 API 响应。

### 特性实现状态

| 特性 | 实现状态 |
|---|---|
| 基于 FastAPI | ✅ |
| 环境配置 | ✅ |
| 直观的用户界面 | ✅ |
| 请求预处理和后处理 | 🚧 |
| 模拟 HTTP 请求 | ✅ |
| 自动化测试 | 🚧 |
| 详细的响应信息 | ✅ |
| 响应时间图表 | ✅ |
| 自定义数据格式 | ✅ |
| 请求模板 | 🚧 |
| 请求加载进度条 | ✅ |
| WebSocket测试 | 🚧 |
| 日志自动分析处理 | 🚧 |
| 可视化数据解析 | 🚧 |
| 请求加密 | 🚧 |
| 国际化支持 | 🚧 |
| API 文档生成 | 🚧 |

## 快速开始

要开始使用 SwiftAPI-Connect，请按照以下步骤操作：

1. **克隆代码库：**

   ```bash
   git clone https://github.com/your_username/SwiftAPI-Connect.git
   ```

2. **安装依赖：**

   ```bash
   cd SwiftAPI-Connect
   pip install -r requirements.txt
   ```

3. **配置环境变量：**

   在项目根目录下创建一个名为 `.env` 的文件，并添加以下内容：

   ```plaintext
   SERVER_HOST=0.0.0.0
   SERVER_PORT=8015
   CORS_ORIGINS=http://localhost:8501
   API_KEY=your_super_secret_key
   ```

   请将 `your_super_secret_key` 替换为您的 API 密钥。

4. **运行应用程序：**

   ```bash
   streamlit run ui/app.py
   ```

5. **访问用户界面：**

   在浏览器中打开 [http://localhost:8501](http://localhost:8501)。

   在 UI 中，您需要输入 API 密钥才能发送请求。

## 贡献

欢迎贡献！如果您有任何想法、建议或发现任何问题，请随时提交 pull request 或开启 issue。

## 许可证

SwiftAPI-Connect 使用 Apache License 2.0 许可。详细信息请参阅 LICENSE 文件。