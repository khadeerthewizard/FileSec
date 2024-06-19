# FileSec: File Integrity Monitoring and Alert System

FileSec is a Python-based graphical user interface (GUI) application designed for file integrity monitoring and real-time alerting. It leverages PowerShell scripts for efficient file hash calculation and comparison to detect unauthorized changes, deletions, or additions within monitored directories.

## Features

- **Baseline Creation and Update**: Automatically generates or updates a baseline CSV file containing file paths and their corresponding SHA-512 hash values to establish a trusted state.
  
- **Real-time Monitoring**: Monitors specified directories continuously to detect any changes compared to the established baseline.
  
- **Alerting Mechanism**: Sends email alerts to specified recipients when unauthorized file changes, deletions, or additions are detected during monitoring.
  
- **User-friendly Interface**: Utilizes tkinter for a simple and intuitive GUI, allowing users to select monitoring options, specify directories, and input email addresses for alerts.

## Technologies Used

- **Python**: Primary programming language used for application logic and GUI development.
  
- **PowerShell**: Scripting language used for efficient file hash calculation and comparison.
  
- **tkinter**: Python's standard GUI toolkit for creating interactive applications.
  
- **smtplib**: Python library for sending email messages from a SMTP server.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/khadeerthewizard/FileSec.git
   cd FileSec
2. **For GUI**
   Install requirements.txt with
   ```bash
   pip install -r requirements.txt

##Usage

1. **Run Application**
    ```bash
    python app.py
    or
    python cli.py

2. **Select the operation**
3. **Receive Alerts on Email**



   
