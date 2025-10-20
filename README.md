# Headlinehub: your multilingual news & sentiment bot 

[![python](https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![telegram](https://img.shields.io/badge/telegram-bot-blue?style=for-the-badge&logo=telegram)](https://telegram.org/)


**Headlinehub** is a smart, python-based telegram bot that scrapes the latest news headlines, performs sentiment analysis, and translates them into your preferred language on demand. get live, emotion-tagged news delivered straight to your chat—simple, intelligent, and multilingual. 🌍

### Demo

here's the bot in action.

**(getting help and instructions)**
<br>
<img src="./images/help_command.png" width="400">

**(fetching and translating news)**
<br>
<img src="./images/translation_example.png" width="400">

###  Core features

-   **1. live web scraping**: fetches top headlines in real-time from bbc news using `requests` and `beautifulsoup`.
-   **2. smart telegram integration**: responds to user commands like `/news` or `/news hi` via the `python-telegram-bot` library.
-   **3. sentiment analysis**: analyzes the mood of each headline (positive, neutral, or negative) using `textblob`.
-   **4. emoji indicators**: visually represents sentiment with corresponding emojis: 😊 (positive), 😐 (neutral), 😞 (negative).
-   **5. multilingual translation**: translates headlines into dozens of languages using the reliable `deep-translator` library.
-   **6. robust error handling**: a global error handler prevents the bot from crashing and provides user-friendly feedback.

###  Commands

| command | description |
| --- | --- |
| `/start` | initializes the bot and shows a welcome message. |
| `/help` | shows the list of commands and how to use them. |
| `/news` | gets the top 10 latest headlines in english. |
| `/news <lang_code>` | gets headlines translated (e.g., `/news hi`, `/news fr`). |

### Setup and installation

1.  **clone the repository:**
    ```bash
    git clone [https://github.com/rajtharun08/headlinehub.git](https://github.com/rajtharun08/headlinehub.git)
    cd headlinehub
    ```

2.  **create and activate a virtual environment:**
    ```bash
    # create the venv
    python -m venv venv
    # activate it (windows)
    venv\scripts\activate
    ```

3.  **install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **download textblob corpora (one-time setup):**
    ```bash
    python -m textblob.download_corpora
    ```

5.  **configure your bot token:**
    create a `.env` file in the root directory and add your telegram bot token:
    ```
    telegram_token="your_telegram_bot_token_here"
    ```

6.  **run the bot:**
    ```bash
    python bot.py
    ```

###  Technologies used

| purpose | library / tool |
| --- | --- |
| web scraping | `beautifulsoup`, `requests` |
| nlp & sentiment | `textblob` |
| translation | `deep-translator` |
| telegram bot | `python-telegram-bot` |
| environment variables | `python-dotenv` |