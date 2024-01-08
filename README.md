
# Mail Encryption Project

## Introduction
HyperSecure is an innovative solution designed to enhance email security through advanced encryption techniques. This project aims to provide a reliable and secure way of communicating over email, ensuring that sensitive information remains confidential. With its robust client and mail-server components, this project is perfect for individuals or organizations looking to secure their email communications.

## Getting Started
To get started with HyperSecure, follow these steps to clone and set up the project on your local machine.

### Prerequisites
- Git
- Python 3.x (for the client component) 
- Node.js (for the server component)
- Any required dependencies listed in `requirements.txt` and `package.json`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/pehlivanoglu/mail_enc.git
   ```
2. Navigate to the project directory:
   ```bash
   cd mail_enc
   ```
3. Install the necessary dependencies:
   - For the mail-server:
     ```bash
     cd mail-server
     npm install
     ```

## Usage
After installation, here's how to run and use the project:
- To start the client application:
  ```bash
  cd client
  source venv/bin/activate
  ```
- To launch the mail-server:
  ```bash
  cd mail-server
  sudo npm run dev
  ```

## Components
### Client
The client component of HyperSecure is a user-friendly terminal interface that allows users to send and receive encrypted emails. It uses advanced cryptographic algorithms to ensure that sensitive information is neither stored nor be seen by malicious users and server-side. It communicates with the mail-server with HTTPS to ensure secure transmission of messages.

### Mail Server
The mail-server component ensures emails are securely transmitted and stored encrypted. Also stores public keys of users for sending mail from client.

## Contributing
We welcome contributions! If you would like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes with clear commit messages.
4. Push to the branch and open a pull request.

## Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the tags on this repository.

## License
This project is not licensed under anything :)
Special thanks to the open-source community for their continuous support.

## Contact
For any queries or contributions, please contact us at [ahmet.pehlivanoglu@ozu.edu.tr](mailto:ahmet.pehlivanoglu@ozu.edu.tr).

## Additional Information
For more information, visit our [Wiki](https://github.com/yourgithubusername/mail_enc/wiki) or check out our [FAQs](https://github.com/yourgithubusername/mail_enc/FAQs).
Actually, we don't have any of these rn :/
