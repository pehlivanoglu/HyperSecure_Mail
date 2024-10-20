
# HYPERSECURE : End to End Encrypted HTTPS Mail Service

## Introduction
HyperSecure is an innovative solution designed to enhance email security through advanced encryption techniques. This project aims to provide a reliable and secure way of communicating over email, ensuring that sensitive information remains confidential. With its robust client and mail-server components, this project is perfect for individuals or organizations looking to secure their email communications.

## Getting Started
To get started with HyperSecure, follow these steps to clone and set up the project on your local machine.

## Prerequisites
- Git
- Python 3.x (for the client component) 
- Node.js (for the server component)
- Any required dependencies listed in mail-server/`package.json`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/pehlivanoglu/HyperSecure_Mail.git
   ```
2. Navigate to the project directory:
   ```bash
   cd HyperSecure_Mail
   ```
3. Install the necessary dependencies:
   For the mail-server:
   ```bash
   cd mail-server
   npm install
   ```
4. Install necessary libs for client side

## Usage
After installation, here's how to run and use the project:
Before running, if you are planning to run the mail-server in your own server, you need to change urls to your machine's url in client/src/apiClient.py
- To start the client application:
  ```bash
  cd client/src
  python3 main.py
  ```
- To launch the mail-server:
  ```bash
  cd mail-server
  sudo npm run dev
  ```

## Components
### Client
The client component of HyperSecure is a user-friendly terminal interface that allows users to send and receive encrypted emails. It uses advanced cryptographic algorithms to ensure that sensitive information is neither stored nor be seen by malicious users and server-side. It communicates with the mail-server via HTTPS to ensure secure transmission of messages.

### Mail Server
The mail-server component ensures that emails are securely transmitted and stored encrypted. Also stores public keys of users for sending mail from client-side.

## Contact
For any queries or contributions, please contact me at [ahmet.pehlivanoglu@ozu.edu.tr](mailto:ahmet.pehlivanoglu@ozu.edu.tr).
