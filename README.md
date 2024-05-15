# Web Requester
[wiki]（https://github.com/riceshowerX/pyc/wiki）

Web Requester is a simple online tool for sending HTTP requests and viewing response results. You can use this tool to send various types of requests and view returned data, error messages, and more.

## Features

- Supports sending GET, POST, PUT, DELETE, HEAD, TRACE, OPTIONS, PATCH, and other request methods.
- Allows adding custom headers and cookies.
- Supports setting an IP proxy address.
- Generates API documentation.
- Includes a stress testing feature.
- Offers WebSocket testing functionality.

## Disclaimer

Web Requester is provided "as is" without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

## Usage

1. Enter the website URL in the URL input box.
2. Select the request method.
3. Enter optional data, such as POST request data.
4. Enter custom headers, cookies, and IP proxy address (optional).
5. Click the "Send Request" button.
6. View the request result and log information.

## Tech Stack

- Backend: FastAPI and aiohttp for handling requests and responses.
- Frontend: HTML, CSS, JavaScript, and jQuery for building the user interface and interaction.

## Installation and Run

1. Clone the project code to your local machine:

   ```bash
   git clone https://github.com/yourusername/web-requester.git
   ```

2. Navigate to the project directory:

   ```bash
   cd web-requester
   ```

3. Create and activate a virtual environment (optional):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate      # Windows
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python run.py
   ```

6. Open a web browser and go to `http://localhost:8000` to see the application.

## Contributing

Contributions and feedback are welcome. Please fork the project, create a new branch for your changes, and then submit a pull request.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
```

Feel free to modify the disclaimer and other sections as needed.