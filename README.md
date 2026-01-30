# SSH Auth Tester

A Python-based SSH authentication testing tool built for **educational and authorized lab environments only**.  
This project demonstrates SSH login handling, threading, and password testing logic for cybersecurity learning.

> ⚠️ Use only on systems you own or have explicit permission to test.

---

## Features
- Multi-threaded SSH authentication testing
- Username list or single username mode
- Password list or password generator
- Colored terminal output
- Retry handling for SSH exceptions
- Saves valid credentials to file

---

## Requirements
- Python 3.8 or higher
- Internet connection (for installing dependencies)
- Linux / Windows / macOS

Disclaimer

This tool is strictly for educational and ethical security research.
Unauthorized access to computer systems is illegal.
The author is not responsible for misuse.

You will be prompted to enter:

Target Host / IP

Username or User List

Password List or Generator

Number of Threads

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ssh-auth-tester.git
cd ssh-auth-tester
python3 -m pip install -r requirements.txt
python3 ssh_credential_tester.py
