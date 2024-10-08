# Web-Based and SSH Honeypot Project

## Overview

This project implements a dual-purpose honeypot system designed to capture unauthorized login attempts and command executions in a controlled environment. It features both a web-based honeypot simulating a WordPress login page and an SSH honeypot that emulates a secure shell interface. By monitoring and logging malicious activities, this project aims to provide insights into common attack patterns and behaviors, enhancing cybersecurity awareness and response strategies.

## Features

### Web-Based Honeypot

- **Simulated Login Page**: 
  - Mimics a WordPress admin login page, enticing attackers to input their credentials. This page is crafted to look authentic, mimicking the structure and design of a typical WordPress interface.
  - **Data Capture**: All usernames, passwords, and IP addresses entered by unauthorized actors attempting to log in are captured and stored securely for further analysis.

- **Dynamic Logging**: 
  - Logs all login attempts—both successful and unsuccessful—into a dedicated log file (`http_audits.log`).
  - **Logging Format**: Each entry includes the timestamp, username, password, and IP address, providing a comprehensive view of attack attempts.

### SSH Honeypot

- **Emulated Shell**: 
  - Provides a realistic command-line interface that mimics a secure shell environment, allowing attackers to execute various commands as if they were interacting with a real server.
  - **Shell Simulation**: Includes common shell functionalities to enhance realism and encourage attackers to engage with the system.

- **Command Logging**: 
  - Every command entered by the attacker is logged in a separate file (`cmd_audits.log`), along with the username and IP address from which the command was issued.
  - **Command Analysis**: This data can be analyzed to determine which commands are frequently attempted, providing insights into the attackers’ objectives.

- **Interactive Responses**: 
  - Responds to specific commands (e.g., `pwd`, `whoami`, and `ls`) with predefined outputs that mimic a legitimate server response.
  - **Purposeful Engagement**: Aims to prolong attackers' engagement, thereby increasing the amount of data captured.

## Libraries Used

The project employs several libraries to facilitate its functionality. Here’s a breakdown of the libraries used, marked in **bold**, along with their purposes:

- **Flask**: 
  - A lightweight WSGI web application framework. It is used to create the web-based honeypot, handling incoming HTTP requests and rendering the simulated login page.
  - **Why**: Flask is easy to set up and is ideal for small applications, making it perfect for creating the honeypot without unnecessary overhead.

- **Flask-Logging**:
  - Provides enhanced logging capabilities for Flask applications.
  - **Why**: This library is essential for logging all HTTP requests and login attempts efficiently, making it easier to maintain logs in a structured format.

- **Paramiko**: 
  - A Python implementation of the SSH protocol. It is used to create the SSH honeypot, allowing the simulation of a secure shell interface.
  - **Why**: Paramiko enables the emulation of SSH connections, allowing us to capture commands executed by attackers seamlessly.

- **Logging**:
  - A standard Python library used for tracking events that happen when the program runs.
  - **Why**: Essential for writing logs to files, helping capture all activities within the honeypot for later analysis.

- **Transporter**: 
  - A utility for transporting data, typically used to send and receive messages in a networked environment.
  - **Why**: In this project, it may be used to facilitate the handling of SSH connections and transport the captured data to the logging system.

## Workflow

1. **Start the Honeypots**: 
   - Initiate either the web-based honeypot or the SSH honeypot based on your requirements.

2. **Capture Unauthorized Access**: 
   - **Web-Based Honeypot**: Attackers attempting to access the login page will have their credentials logged.
   - **SSH Honeypot**: Any commands executed by the attacker will be logged in real-time.

3. **Analyze Logs**: 
   - Review the log files (`http_audits.log`, `audits.log`, and `cmd_audits.log`) for valuable information regarding captured credentials, attempted logins, and executed commands.

## Installation

To install the required packages and set up the honeypot project, follow these steps:

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/yourusername/honeypot.git
   cd honeypot

2. **Set Up a Virtual Environment (Optional but Recommended):**: 
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Required Packages:**: 
   ```bash
    pip install -r requirements.txt

4. **Run the HoneyPots**: 
   ```bash
   python web_honeypot.py  # For web-based honeypot
   python ssh_honeypot.py  # For SSH honeypot
   
