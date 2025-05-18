🪙 CryptoWise – Smart Crypto Learning & Trading
CryptoWise is a Streamlit-based web application that enables users to learn, explore, and simulate crypto trading in a multilingual, user-friendly environment. The app uses Object-Oriented Programming (OOP) principles and simulates core crypto functionalities including registration, login, trading, language preferences, and reminders.

🚀 Features
🔐 User Authentication (Register/Login)

💱 Simulated Crypto Trading Desk

🌍 Multilingual Support (English, Urdu, Roman Urdu)

📊 Trading History

⏰ Set Crypto Price Reminders

🖼️ Image Upload and Viewer

🧠 Educational Sections:

Benefits of Crypto Trading

Risks in Crypto Trading

Smart Solutions

🧑‍💻 Object-Oriented Structure for User and Market logic

🏗️ Project Structure & OOP Usage
This app uses OOP principles through two main classes:

User class
Encapsulates all user-related logic:

Stores username, email, hashed_password, and language

Validates password with a secure hash

CryptoMarket class
Handles:

Current simulated crypto prices

Fetching live price (from static dictionary for now)

get_localized_text()
Handles i18n (internationalization) based on the user's selected language.

📦 Technologies Used
Streamlit for UI

hashlib, uuid for security logic🌐 Languages Supported
🇺🇸 English

🇵🇰 Urdu

🔤 Roman Urdu

datetime for timestamps

pandas for data handling

OOP in Python to manage structure and logic

📚 Educational Value
CryptoWise isn't just a trading simulation tool – it's also an educational platform. Users can explore:

Pros and cons of crypto

Security best practices

Simulated trading before jumping into real markets

🛡️ Disclaimer
This is a simulated trading platform and does not use real cryptocurrencies or financial transactions. Always do your own research before investing in real assets.

📬 Feedback & Contributions
If you have suggestions, new language translations, or want to improve features — feel free to open issues or submit a pull request!
