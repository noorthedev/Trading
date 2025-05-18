import streamlit as st
from datetime import datetime
import hashlib
import uuid
import json
import pandas as pd
from io import BytesIO

# --------------------------
# Simulated Data & Classes
# --------------------------

class User:
    def __init__(self, user_id, username, email, hashed_password, language="en"):
        self.user_id = user_id
        self.username = username
        self.email = email
        self._hashed_password = hashed_password
        self.language = language  # User language preference

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest() == self._hashed_password

    def set_language(self, language):
        self.language = language

class CryptoMarket:
    def __init__(self):
        self.prices = {
            'Bitcoin': 64000,
            'Ethereum': 3100,
            'Solana': 150,
            'Ripple': 0.65
        }

    def get_price(self, coin):
        return self.prices.get(coin, 'N/A')

# --------------------------
# Helper Functions
# --------------------------

def hash_password(password):
    """
    Hashes the password using SHA256. Use bcrypt in a real application.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def get_localized_text(language, key):
    """
    Retrieves text based on the selected language.
    """
    translations = {
        "en": {
            "home_title": "Welcome to CryptoWise",
            "home_text": "A platform to learn, explore, and trade cryptocurrency securely. Your gateway to smart digital wealth.",
            "register_title": "Create Your Account",
            "login_title": "Login to Your Account",
            "trading_title": "Live Trading Desk",
            "benefits_title": "Benefits of Crypto Trading",
            "risks_title": "Risks in Crypto Trading",
            "solutions_title": "Smart Solutions",
            "logout_message": "You have been logged out.",
            "username_label": "Username",
            "email_label": "Email",
            "password_label": "Password",
            "register_button": "Register",
            "login_button": "Login",
            "amount_label": "Amount in USD",
            "buy_now_button": "Buy Now",
            "select_coin_label": "Select Coin",
            "current_price_label": "Current",
            "invalid_credentials": "Invalid credentials.",
            "username_exists": "Username already exists.",
            "logout_button": "Logout",
            "reminder_title": "Set Reminder",
            "reminder_text": "Remind me about crypto prices:",
            "1_day_ago": "1 Day Ago",
            "1_year_ago": "1 Year Ago",
            "previous_prices": "Previous Prices",
            "download_data": "Download Data",
            "settings_title": "Settings",
            "language_setting": "Select Language",
            "language_en": "English",
            "language_ur": "Urdu",
            "language_ru": "Roman Urdu",
            "upload_image_title": "Upload Image",
            "image_details_title": "Image Details",
            "no_image_uploaded": "No image uploaded yet.",
            "error_image_upload": "Error uploading image.",
            "error_amount_less_than_0": "Amount must be greater than 0.",
            "required_field": "This field is required",
            "bitcoin_trading_image_title": "Bitcoin Trading",
            "image_click_message": "Click on the image to see details.",
        },
        "ur": {
            "home_title": "CryptoWise میں خوش آمدید",
            "home_text": "محفوظ طریقے سے کریپٹو کرنسی سیکھنے، دریافت کرنے اور تجارت کرنے کا ایک پلیٹ فارم۔ آپ کی ڈیجیٹل دولت کا گیٹ وے۔",
            "register_title": "اپنا اکاؤنٹ بنائیں",
            "login_title": "اپنے اکاؤنٹ میں لاگ ان کریں",
            "trading_title": "لائیو ٹریڈنگ ڈیسک",
            "benefits_title": "کریپٹو ٹریڈنگ کے فوائد",
            "risks_title": "کریپٹو ٹریڈنگ میں خطرات",
            "solutions_title": "اسمارٹ حل",
            "logout_message": "آپ لاگ آؤٹ ہو گئے ہیں۔",
            "username_label": "صارف نام",
            "email_label": "ای میل",
            "password_label": "پاس ورڈ",
            "register_button": "رجسٹر کریں",
            "login_button": "لاگ ان کریں",
            "amount_label": "USD میں مقدار",
            "buy_now_button": "ابھی خریدیں",
            "select_coin_label": "سکہ منتخب کریں",
            "current_price_label": "موجودہ قیمت",
            "invalid_credentials": "غلط اسناد۔",
            "username_exists": "صارف نام پہلے سے موجود ہے۔",
            "logout_button": "لاگ آؤٹ",
            "reminder_title": "یاد دہانی سیٹ کریں",
            "reminder_text": "مجھے کریپٹو کی قیمتوں کے بارے میں یاد دلائیں:",
            "1_day_ago": "1 دن پہلے",
            "1_year_ago": "1 سال پہلے",
            "previous_prices": "پچھلی قیمتیں",
            "download_data": "ڈیٹا ڈاؤن لوڈ کریں",
            "settings_title": "ترتیبات",
            "language_setting": "زبان منتخب کریں",
            "language_en": "انگریزی",
            "language_ur": "اردو",
            "language_ru": "رومن اردو",
            "upload_image_title": "تصویر اپ لوڈ کریں",
            "image_details_title": "تصویر کی تفصیلات",
            "no_image_uploaded": "کوئی تصویر اپ لوڈ نہیں کی گئی۔",
            "error_image_upload": "تصویر اپ لوڈ کرنے میں خرابی۔",
            "error_amount_less_than_0": "مقدار 0 سے زیادہ ہونی چاہیے۔",
            "required_field": "یہ فیلڈ ضروری ہے",
            "bitcoin_trading_image_title": "بٹ کوائن ٹریڈنگ",
            "image_click_message": "تفصیلات دیکھنے کے لیے تصویر پر کلک کریں۔",
        },
        "ru": {
            "home_title": "CryptoWise میں خوش آمدید",
            "home_text": "محفوظ طریقے سے کریپٹو کرنسی سیکھنے، دریافت کرنے اور تجارت کرنے کا ایک پلیٹ فارم۔ آپ کی ڈیجیٹل دولت کا گیٹ وے۔",
            "register_title": "اپنا اکاؤنٹ بنائیں",
            "login_title": "اپنے اکاؤنٹ میں لاگ ان کریں",
            "trading_title": "لائیو ٹریڈنگ ڈیسک",
            "benefits_title": "کریپٹو ٹریڈنگ کے فوائد",
            "risks_title": "کریپٹو ٹریڈنگ میں خطرات",
            "solutions_title": "اسمارٹ حل",
            "logout_message": "آپ لاگ آؤٹ ہو گئے ہیں۔",
            "username_label": "یوزرنیم",
            "email_label": "ای میل",
            "password_label": "پاس ورڈ",
            "register_button": "رجسٹر کریں",
            "login_button": "لاگ ان کریں",
            "amount_label": "USD میں مقدار",
            "buy_now_button": "ابھی خریدیں",
            "select_coin_label": "سکہ منتخب کریں",
            "current_price_label": "موجودہ قیمت",
            "invalid_credentials": "غلط اسناد۔",
            "username_exists": "یوزرنیم پہلے سے موجود ہے۔",
            "logout_button": "لاگ آؤٹ",
            "reminder_title": "یاد دہانی سیٹ کریں",
            "reminder_text": "مجھے کریپٹو کی قیمتوں کے بارے میں یاد دلائیں:",
            "1_day_ago": "1 دن پہلے",
            "1_year_ago": "1 سال پہلے",
            "previous_prices": "پچھلی قیمتیں",
            "download_data": "ڈیٹا ڈاؤن لوڈ کریں",
            "settings_title": "ترتیبات",
            "language_setting": "زبان منتخب کریں",
            "language_en": "انگریزی",
            "language_ur": "اردو",
            "language_ru": "رومن اردو",
            "upload_image_title": "تصویر اپ لوڈ کریں",
            "image_details_title": "تصویر کی تفصیلات",
            "no_image_uploaded": "کوئی تصویر اپ لوڈ نہیں کی گئی۔",
            "error_image_upload": "تصویر اپ لوڈ کرنے میں خرابی۔",
            "error_amount_less_than_0": "مقدار 0 سے زیادہ ہونی چاہیے۔",
            "required_field": "یہ فیلڈ ضروری ہے",
            "bitcoin_trading_image_title": "بٹ کوائن ٹریڈنگ",
            "image_click_message": "تفصیلات دیکھنے کے لیے تصویر پر کلک کریں۔",
        },
    }
    return translations.get(language, translations["en"]).get(key, key) # Default to English if not found

# --------------------------
# Initialize or get session state variables
# --------------------------

if 'users' not in st.session_state:
    st.session_state['users'] = {}

if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = None

if 'language' not in st.session_state:
    st.session_state['language'] = "en"  # Default language

if 'uploaded_image' not in st.session_state:
    st.session_state['uploaded_image'] = None

# Initialize market instance
market = CryptoMarket()

# --------------------------
# Streamlit App Starts Here
# --------------------------

st.set_page_config(page_title="CryptoWise", layout="centered")
st.title("\U0001F4B0 CryptoWise - Smart Crypto Learning & Trading")

menu = ["Home", "Register", "Login", "Trading", "Benefits", "Risks", "Solutions", "Logout", "Settings", "Reminder",  "Download", "Crypto details"]
choice = st.sidebar.selectbox("Navigate", menu)

# Show logged in user in sidebar
if st.session_state['logged_in_user']:
    st.sidebar.markdown(f"**Logged in as:** {st.session_state['logged_in_user']}")

# --------------------------
# Pages
# --------------------------

def register():
    st.subheader(get_localized_text(st.session_state['language'], "register_title"))
    username = st.text_input(get_localized_text(st.session_state['language'], "username_label"), key="reg_username")
    email = st.text_input(get_localized_text(st.session_state['language'], "email_label"), key="reg_email")
    password = st.text_input(get_localized_text(st.session_state['language'], "password_label"), type="password", key="reg_password")

    if st.button(get_localized_text(st.session_state['language'], "register_button")):
        if not username:
            st.error(get_localized_text(st.session_state['language'], "required_field"))
            return
        if not email:
            st.error(get_localized_text(st.session_state['language'], "required_field"))
            return
        if not password:
            st.error(get_localized_text(st.session_state['language'], "required_field"))
            return
        if username in st.session_state['users']:
            st.error(get_localized_text(st.session_state['language'], "username_exists"))
        else:
            user_id = str(uuid.uuid4())
            hashed_password = hash_password(password)
            language = st.session_state['language']
            st.session_state['users'][username] = User(user_id, username, email, hashed_password, language)
            st.success("Registered successfully. You can now login.")

def login():
    st.subheader(get_localized_text(st.session_state['language'], "login_title"))
    username = st.text_input(get_localized_text(st.session_state['language'], "username_label"), key="login_username")
    password = st.text_input(get_localized_text(st.session_state['language'], "password_label"), type="password", key="login_password")

    if st.button(get_localized_text(st.session_state['language'], "login_button")):
        if not username:
            st.error(get_localized_text(st.session_state['language'], "required_field"))
            return
        if not password:
            st.error(get_localized_text(st.session_state['language'], "required_field"))
            return

        user = st.session_state['users'].get(username)
        if user and user.check_password(password):
            st.session_state['logged_in_user'] = username
            st.success(f"Welcome back, {username}!")
        else:
            st.error(get_localized_text(st.session_state['language'], "invalid_credentials"))

def logout():
    st.session_state['logged_in_user'] = None
    st.success(get_localized_text(st.session_state['language'], "logout_message"))

def trading():
    st.subheader(get_localized_text(st.session_state['language'], "trading_title"))

    if not st.session_state['logged_in_user']:
        st.warning("Please login first to access trading.")
        return

    coin = st.selectbox(get_localized_text(st.session_state['language'], "select_coin_label"), list(market.prices.keys()))
    price = market.get_price(coin)
    st.info(f"{get_localized_text(st.session_state['language'], 'current_price_label')} {coin} : ${price}")

    amount = st.number_input(get_localized_text(st.session_state['language'], "amount_label"), min_value=10.0)

    if st.button(get_localized_text(st.session_state['language'], "buy_now_button")):
        if amount > 0:
            st.success(f"You bought ${amount} worth of {coin} at ${price}!")

            # Record trade in trading history
            trade = {
                "user": st.session_state['logged_in_user'],
                "coin": coin,
                "amount": amount,
                "price": price,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            if "trading_history" not in st.session_state:
                st.session_state["trading_history"] = []

            st.session_state["trading_history"].append(trade)
        else:
            st.error(get_localized_text(st.session_state['language'], "error_amount_less_than_0"))

def benefits():
    st.subheader(get_localized_text(st.session_state['language'], "benefits_title"))
    st.markdown("""
    - High return potential
    - Decentralized & transparent
    - Borderless transactions
    - 24/7 market access
    """)

def risks():
    st.subheader(get_localized_text(st.session_state['language'], "risks_title"))
    st.markdown("""
    - Volatility
    - Regulatory uncertainty
    - Scams & frauds
    - Irreversible transactions
    """)
# solutions
def solutions():
    st.subheader(get_localized_text(st.session_state['language'], "solutions_title"))
    st.markdown("""
    - Use trusted wallets & exchanges
    - Diversify investments
    - Stay updated with market news
    - Practice secure password habits
    """)

def home():
    st.image("https://www.shutterstock.com/image-photo/technical-price-graph-indicator-red-600nw-2159962175.jpg", width=100)
    st.markdown(get_localized_text(st.session_state['language'], "home_title"))
    st.markdown(get_localized_text(st.session_state['language'], "home_text"))

def show_image_details(image_data):
    """
    Displays details of the uploaded image.
    """
    if image_data:
        st.image(image_data, caption="Uploaded Image", use_container_width=True)
        st.write(f"Image Size: {len(image_data)} bytes")
        #  Add more image analysis here (e.g., using PIL) if needed
    else:
        st.write(get_localized_text(st.session_state['language'], "no_image_uploaded"))


#  crypto_details
def crypto_details():

    if "trading_history" not in st.session_state:
        st.session_state["trading_history"] = []

    if "logged_in_user" not in st.session_state:
        st.error("Please log in to view your trading history.")
        return

    history = [t for t in st.session_state["trading_history"] if t["user"] == st.session_state["logged_in_user"]]
    # aap ka baqi ka logic yahaan...

    st.subheader("📈 Crypto Trading History")

    if not st.session_state['logged_in_user']:
        st.warning("Please login to view your trading history.")
        return

    history = [t for t in st.session_state['trading_history'] if t['user'] == st.session_state['logged_in_user']]
    
    if history:
        df = pd.DataFrame(history)
        df = df[["timestamp", "coin", "price", "amount"]]
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label=get_localized_text(st.session_state['language'], "download_data"),
                           data=csv,
                           file_name='trading_history.csv',
                           mime='text/csv')
    else:
        st.info("No trading history available.")

    crypto_data = {
        "Bitcoin (BTC)": {
            "💡 What is it?": "Bitcoin is the first and most popular cryptocurrency, created in 2009 by Satoshi Nakamoto.",
            "🔐 Key Features:": [
                "Decentralized: No government or bank controls it.",
                "Limited Supply: Only 21 million BTC will ever exist.",
                "Blockchain-based: All transactions are recorded on a public digital ledger.",
                "Secure & Transparent: Once recorded, transactions cannot be changed."
            ],
            "📈 Common Uses:": [
                "Digital investment (like gold)",
                "Cross-border payments",
                "Store of value (used as digital gold)"
            ]
        },
        "Ethereum (ETH)": {
            "💡 What is it?": "Ethereum is a blockchain platform launched in 2015 by Vitalik Buterin, with its own cryptocurrency called Ether (ETH).",
            "🔐 Key Features:": [
                "Smart Contracts: Self-executing agreements stored on the blockchain.",
                "Decentralized Apps (dApps): Used to build DeFi, NFTs, games, and more.",
                "Ether is used to pay for transactions and computational services on the Ethereum network."
            ],
            "🔧 Why it’s powerful:": [
                "It’s the foundation for most Web3 projects.",
                "Home to most NFTs, DeFi apps, and tokens."
            ]
        },
        "Solana (SOL)": {
            "💡 What is it?": "Solana is a high-performance blockchain launched in 2020, designed for speed and low fees.",
            "⚡ Key Features:": [
                "Ultra-fast: Can handle 65,000+ transactions per second (TPS).",
                "Low transaction fees: Fractions of a penny per transaction.",
                "Proof of History (PoH) + Proof of Stake (PoS): Combines speed with security."
            ],
            "📱 Use Cases:": [
                "DeFi platforms",
                "NFT marketplaces",
                "Blockchain gaming"
            ],
            "✅ Known For:": [
                "Competing with Ethereum as a faster and cheaper alternative."
            ]
        },
        "Ripple (XRP)": {
            "💡 What is it?": "Ripple is both a company and a cryptocurrency (XRP), focused on enabling real-time, low-cost international money transfers.",
            "💸 Key Features:": [
                "Used by banks and financial institutions to transfer money globally.",
                "Transaction time: Just 3-5 seconds",
                "Low energy usage compared to Bitcoin"
            ],
            "🔍 Unique Point:": [
                "It’s not fully decentralized — Ripple Labs controls part of the network.",
                "XRP is suited for enterprise-level payments more than individual use."
            ]
        }
    }

    st.title("Click to Explore Cryptocurrencies")

    for name, details in crypto_data.items():
        with st.expander(f"🔹 {name}"):
            for key, value in details.items():
                st.subheader(key)
                if isinstance(value, list):
                    for item in value:
                        st.markdown(f"- {item}")
                else:
                    st.markdown(value)

    st.subheader("🔚 Summary Table:")
    st.markdown("""
    | Crypto    | Launch Year | Speed      | Use Case                          | Special Feature                 |
    |-----------|-------------|------------|-----------------------------------|---------------------------------|
    | Bitcoin   | 2009        | Slow       | Digital gold, investments         | Limited supply (21M BTC)        |
    | Ethereum  | 2015        | Medium     | Smart contracts, dApps, NFTs      | Most popular Web3 platform      |
    | Solana    | 2020        | Super Fast | Fast dApps, DeFi, NFTs           | 65K+ TPS, low fees              |
    | Ripple    | 2012        | Very Fast  | Global bank-to-bank transfers     | Enterprise finance focused      |
    """)


# Reminder
class ReminderApp:
    def __init__(self):
        if 'reminders' not in st.session_state:
            st.session_state['reminders'] = []

    def set_reminder(self):
        st.subheader("⏰ Set Reminder")

        if not st.session_state['logged_in_user']:
            st.warning("Please login to set a reminder.")
            return

        reminder_msg = st.text_input("Reminder Message")
        reminder_time = st.time_input("Reminder Time (Today)")

        now = datetime.now()
        reminder_datetime = datetime.combine(now.date(), reminder_time)

        if st.button("Set Reminder"):
            if reminder_datetime <= now:
                st.error("Reminder time must be in the future.")
            else:
                st.success(f"Reminder set for {reminder_time.strftime('%H:%M:%S')}")
                self._add_reminder(st.session_state['logged_in_user'], reminder_msg, reminder_datetime.strftime('%Y-%m-%d %H:%M:%S'))

    def _add_reminder(self, user, message, time):
        st.session_state['reminders'].append({
            'user': user,
            'message': message,
            'time': time
        })

    def display_reminders(self):
        if 'reminders' in st.session_state:
            st.subheader("📋 Your Reminders")
            for reminder in st.session_state['reminders']:
                if reminder['user'] == st.session_state['logged_in_user']:
                    st.write(f"🕒 {reminder['time']} - {reminder['message']}")


class DataDownloader:
    def __init__(self):
        self.data = {
            "Name": ["Alice", "Bob", "Charlie", "Anum", "Noor"],
            "Age": [25, 30, 35, 22, 24],
            "City": ["New York", "London", "Tokyo", "Pakistan", "India"]
        }
        self.df = pd.DataFrame(self.data)

    def download_data_ui(self, get_localized_text, language):
        st.subheader(get_localized_text(language, "download_data"))
        file_format = st.selectbox("Select format", ["JSON", "CSV", "Excel"])

        if st.button("Download"):
            if file_format == "JSON":
                self._download_json()
            elif file_format == "CSV":
                self._download_csv()
            elif file_format == "Excel":
                self._download_excel()

    def _download_json(self):
        json_data = self.df.to_json(orient="records")
        st.download_button(
            label="Download JSON",
            data=json_data.encode("utf-8"),
            file_name="data.json",
            mime="application/json"
        )

    def _download_csv(self):
        csv_data = self.df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv_data.encode("utf-8"),
            file_name="data.csv",
            mime="text/csv"
        )

    def _download_excel(self):
        excel_buffer = BytesIO()
        self.df.to_excel(excel_buffer, index=False)
        excel_data = excel_buffer.getvalue()
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name="data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


class SettingsManager:
    def display_settings(self, get_localized_text, language):
        st.subheader(get_localized_text(language, "settings_title"))
        language_options = {
            "en": get_localized_text(language, "language_en"),
            "ur": get_localized_text(language, "language_ur"),
            "ru": get_localized_text(language, "language_ru"),
        }
        selected_language = st.selectbox(
            get_localized_text(language, "language_setting"),
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
        )
        st.session_state['language'] = selected_language


# --------------------------
# Navigation Routing
# --------------------------

if choice == "Home":
    home()
elif choice == "Register":
    register()
elif choice == "Login":
    login()
elif choice == "Logout":
    logout()
elif choice == "Trading":
    trading()
elif choice == "Benefits":
    benefits()
elif choice == "Risks":
    risks()
elif choice == "Solutions":
    solutions()
elif choice == "Settings":
    SettingsManager().display_settings(get_localized_text, st.session_state['language'])
elif choice == "Reminder":
    def reminder():
        app = ReminderApp()
        app.set_reminder()
        app.display_reminders()
    reminder()
elif choice == "Previous":
    def reminder():
        app = ReminderApp()
        app.set_reminder()
        app.display_reminders()
    reminder() # combined
elif choice == "Download":
    DataDownloader().download_data_ui(get_localized_text, st.session_state['language'])
elif choice == "Crypto details":
   crypto_details()


if __name__ == "__main__":
    pass