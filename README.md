# 🔐 Admin Panel Brute Force Tool v2.0

Admin Panel Brute Force Tool is a testing tool designed to evaluate the security of web applications. This tool aims to attempt login to the target system using a trial-and-error method with username and password combinations. It is intended for use in security testing.

**⚠️ Legal Disclaimer:** This tool should only be used on systems you have explicit permission to test. Unauthorized use is illegal and unethical. The responsibility for using this tool lies entirely with the user.

---

## 🚀 Features
- Automatically tests username and password combinations.
- Saves successful login attempts.
- Configurable HTTP request headers.
- Option to disable SSL verification warnings.
- Timeout and delay control between requests.
- Custom criteria for detecting successful logins.
- User-friendly and colorful interface.

---

## 🛠️ Installation

To use this tool, follow the steps below:

### 1. Requirements
- Python 3.8 or higher
- Pip package manager

### 2. Install Required Libraries

Install the necessary libraries using the following command:

```bash
pip install -r requirements.txt
```

**requirements.txt content:**
```
requests
colorama
```

### 3. Clone the Project

```bash
git clone https://github.com/username/bruteforce-tool.git
cd bruteforce-tool
```

### 4. Start the Tool

Run the tool using the following command:

```bash
python bruteforce_tool.py
```

---

## 📋 Usage

### 1. Main Menu
When you start the tool, you will see the following menu:
- **[1] Set URL:** Specify the target admin panel login URL.
- **[2] Set Wordlist:** Choose the file containing username and password combinations.
- **[3] Start Attack:** Launch the brute force attack with the specified settings.
- **[4] Show Settings:** Display the current configuration.
- **[5] Exit:** Exit the program.

### 2. Configure Settings
- **Set URL:** Specify the login panel URL of the target system.
- **Wordlist:** Provide a file containing username and password combinations in the "username:password" format.

### 3. Start Brute Force Attack
- When you start the attack, each combination will be tested, and successful logins will be logged.
- Successful logins are saved in the `successful_logins.txt` file.

---

## 📂 Project Structure

```
.
├── bruteforce_tool.py      # Main Python file
├── giris.txt               # Wordlist file (example)
├── successful_logins.txt   # File for storing successful logins
├── bruteforce_log.txt      # Log file
└── requirements.txt        # Required Python libraries
```

---

## ⚙️ Customization
You can customize the following variables in the `bruteforce_tool.py` file:
- **`self.timeout`**: Timeout duration for HTTP requests.
- **`self.min_delay` / `self.max_delay`**: Minimum and maximum delay between requests.
- **`self.success_criteria`**: Response text criteria for a successful login.

---

## 📖 License
This project is licensed under the MIT License. For more details, see the `LICENSE` file.

---

## 💡 Notes
- This tool should only be used by authorized personnel for security testing purposes.
- Unauthorized access and testing are illegal.

