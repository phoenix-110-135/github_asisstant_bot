# GitHub Bot README

## 📜 Overview
This is a Telegram bot designed to assist users with their GitHub profiles and create README.md files for their projects. The bot supports both Persian and English languages, allowing users to interact in their preferred language. 

## 🚀 Features
- **User Registration**: Automatically registers users in a SQLite database when they start the bot.
- **Language Selection**: Users can choose between Persian and English for interaction.
- **Admin Panel**: Admins can send messages and images to all users, view user statistics, and send messages to individual users.
- **GitHub Profile Information**: Users can input their GitHub username to retrieve their profile information, including followers, following, number of repositories, and bio.
- **README.md Creation**: Users can provide project details, and the bot generates a formatted README.md file.

## 🛠️ Technologies Used
- **Python**: The primary programming language.
- **SQLite**: For database management.
- **BeautifulSoup**: For web scraping GitHub profiles.
- **Pillow**: For image processing.
- **Requests**: To handle HTTP requests.

## 📦 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/phoenix-110-135/github_assistant_bot.git
   ```
2. Navigate to the project directory:
   ```bash
   cd github_assistant_bot
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. run bale bot :
   ```bash
   python github_assistant_bale.py
   ```
5. run telegram bot :
   ```bash
   python github_assistant_telegram.py
   ```
## ⚙️ Configuration
- Ensure to replace the bot token in the code with your own:
  ```python
  bot = Bot(token="YOUR_BOT_TOKEN")
  ```

## 📧 Usage
1. Start the bot on Telegram by searching for its username and clicking "Start".
2. Select your preferred language.
3. Follow the prompts to interact with the bot.

## 👤 Admin Commands
- `/admin`: Access the admin panel (restricted to authorized users).
- Various buttons for sending messages, viewing statistics, and more.

## 📄 Example README.md Structure
When prompted, you can provide details in the following format:
```
Project Title: Your Project Name
Description: A brief overview of what the project does and its purpose.
Table of Contents: A list of sections included in the README.
Installation: Instructions on how to install the project, including any dependencies.
Usage: Examples of how to use the project, including code snippets.
Contributing: Guidelines for contributing to the project.
License: Information about the project's license.
```

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## 📞 Support
For support, please contact [a87h97@gmail.com](mailto:a87h97@gmail.com).