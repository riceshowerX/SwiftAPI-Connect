<div align="center" style="display: flex; align-items: center;">
  <img src="https://riceshowerX.github.io/picx-images-hosting/社交头像.3yeal59d7b.webp" alt="Logo" width="70" height="70" style="margin-right: 10px;"> 
  <h1> SwiftAPI-Connect </h1> 
</div>

<p align="center">
  🚀 **SwiftAPI-Connect 是一款基于 FastAPI 的多功能网站请求工具，旨在简化和加速您的 Web 开发流程！** 
</p>

<p align="center">
  <a href="https://github.com/riceshowerX/SwiftAPI-Connect/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0"></a>
  <a href="https://github.com/riceshowerX/SwiftAPI-Connect/releases/latest"><img src="https://img.shields.io/github/v/release/riceshowerX/SwiftAPI-Connect" alt="Latest Release"></a>
  <a href="https://github.com/riceshowerX/SwiftAPI-Connect/issues"><img src="https://img.shields.io/github/issues/riceshowerX/SwiftAPI-Connect" alt="Open Issues"></a>
  <a href="https://github.com/riceshowerX/SwiftAPI-Connect/pulls"><img src="https://img.shields.io/github/issues-pr/riceshowerX/SwiftAPI-Connect" alt="Pull Requests"></a>
</p>

## ✨ 主要特性

- **🚀 高性能请求引擎:**  基于 FastAPI 构建，提供快速且高效的网站请求体验。
- **🖥️  直观的用户界面:**  提供易于使用的界面，用于构建请求、发送请求和查看结果，无需编写代码即可测试您的网站。
- **🌐 多种请求方法:** 支持 GET、POST、PUT、DELETE 等所有常见的 HTTP 请求方法，满足您的各种测试需求。
- **📊 详细的性能指标:**  提供丰富的性能指标，包括响应时间、状态码、请求头、响应头等，帮助您深入分析网站性能。
- **🔐 安全可靠:** 支持 API 密钥验证等安全机制，确保您的请求安全可靠。 
- **⚙️  灵活易用:**  支持自定义请求头、请求体、数据格式等，满足您个性化的测试需求。

## 快速开始

1. **克隆代码库:**

   ```bash
   git clone https://github.com/riceshowerX/SwiftAPI-Connect.git
   ```
   
2. **安装依赖:**

   ```bash
   cd SwiftAPI-Connect
   pip install -r requirements.txt
   ```

3. **配置环境变量:**

   在项目根目录下创建一个名为 `.env` 的文件，并添加以下内容:

   ```env
   PYTHONPATH=你的项目路径
   SERVER_HOST=127.0.0.1
   SERVER_PORT=8015
   CORS_ORIGINS=http://localhost:8501
   API_KEY=your_super_secret_key
   ```

   请将 `your_super_secret_key` 替换为您的 API 密钥。您无需手动设置加密密钥，UI 界面会自动生成一个新的密钥。

4. **启动 SwiftAPI-Connect:**

   运行应用程序:

   ```bash
   streamlit run ui/main_ui.py
   ```

5. **访问用户界面:**

   在浏览器中打开 [http://localhost:8501](http://localhost:8501)。

   在 UI 中，您需要输入 API 密钥才能发送请求。您也可以选择是否开启加密功能。

## 特性实现状态

| 特性                 | 实现状态 |
|----------------------|----------|
| 基于 FastAPI         | ✅       |
| 环境配置             | ✅       |
| 直观的用户界面       | ✅       |
| 请求预处理和后处理   | ✅       |
| 模拟 HTTP 请求       | ✅       |
| 自动化测试           | ❌       |
| 详细的响应信息       | ✅       |
| 响应时间图表         | ✅       |
| 自定义数据格式       | ✅       |
| 请求模板             | ❌       |
| 请求加载进度条       | ❌       |
| WebSocket 测试       | ❌       |
| 日志自动分析处理     | ❌       |
| 可视化数据解析       | ❌       |
| 请求加密             | ✅       |
| 国际化支持           | ❌       |
| API 文档生成         | ❌       |

## 贡献

我们热烈欢迎您的贡献！
如果您有任何想法、建议或发现任何问题，请随时提交 pull request 或开启 issue。

本项目由个人在业余时间开发和维护，因此开发和修复进度可能较慢，且不定期进行更新。我们感谢您的理解和支持，并欢迎通过提交 issue 或 pull request 来帮助改进项目。

## 许可证

SwiftAPI-Connect 使用 Apache License 2.0 许可。详细信息请参阅 [LICENSE](https://github.com/riceshowerX/SwiftAPI-Connect/blob/main/LICENSE) 文件。

## 免责声明

本项目按“原样”提供，不附带任何明示或暗示的保证。具体而言，包括但不限于针对适销性、特定用途的适用性和不侵权的保证。用户在使用本项目时需自行承担风险。

在任何情况下，本项目的作者和贡献者均不对因使用或无法使用本软件而导致的任何形式的损失或损害负责，包括但不限于以下几种情况：

- 直接损失或损害: 包括但不限于数据丢失、业务中断或设备损坏。
- 间接损失或损害: 包括但不限于收入损失、利润损失、预期储蓄损失、业务损失、机会损失、商誉或声誉损失。
- 偶发性、特殊性、后果性或惩罚性损害: 无论是由于合同、侵权行为（包括过失）或其他原因造成的。
- 第三方索赔: 包括但不限于第三方因使用本软件而对用户提出的任何索赔或诉讼。

无论作者或贡献者是否已被告知可能发生此类损害，这些免责条款在任何情况下均适用。用户应在使用本软件之前自行评估其适用性，并采取必要的预防措施来保护其系统和数据安全。用户需了解并同意，本项目的开发者和贡献者在提供此软件时，不承担任何形式的责任。

用户在使用本项目时，应充分认识到以下几点：

- 风险自负: 用户应自行承担使用本项目的所有风险，包括但不限于与本软件相关的任何故障、问题或损害。
- 预防措施: 用户有责任在使用本项目之前采取一切必要的预防措施来保护其系统和数据的安全性。
- 独立评估: 用户需自行评估本项目的适用性和安全性，确保其符合自身需求。

用户在使用本项目的过程中出现的任何问题、故障或损害，均由用户自行负责，开发者和贡献者概不负责。通过使用本项目，用户即表示已阅读并同意上述所有条款和条件。
