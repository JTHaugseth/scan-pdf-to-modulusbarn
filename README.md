
# PDF to ModulusBarn Uploader

This project monitors a folder for newly added PDF files, processes them, and uploads them to the **ModulusBarn API**. It handles successful and failed uploads by organizing files into respective folders and logs the process for reference.

---

## 📋 Prerequisites

### 1. **Python Installation**
- Ensure you have Python 3.8 or later installed on your system.
- Download Python from [python.org](https://www.python.org/downloads/).

### 2. **Pip Installation**
- Pip, Python's package installer, is included by default with most Python installations.
- Verify pip installation by running:
  ```bash
  pip --version
  ```

### 3. **Required Libraries**
Install the following Python libraries using pip:
```bash
pip install watchdog requests pyjwt cryptography
```

- **`watchdog`**: Monitors the filesystem for changes.
- **`requests`**: Handles HTTP requests to the ModulusBarn API.
- **`pyjwt`**: Used for generating JSON Web Tokens (JWTs).
- **`cryptography`**: Handles private key management for JWT signing.

---

## 📁 Project Structure

```plaintext
project-folder/
│
├── privatekey.pem        # Private key file for signing JWTs (Enterprise Certificate (Virksomhetssertifikat))
├── log/                  # Logs successful uploads
├── scan-entry/           # Folder monitored for new PDFs
├── scan-failed/          # PDFs moved here after failed uploads
├── scan-finished/        # PDFs moved here after successful uploads
├── token_handler.py      # Generates and retrieves access tokens
└── main.py               # Main script for monitoring and uploading PDFs
```

---

## 🚀 How to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/JTHaugseth/scan-pdf-to-modulusbarn.git
   cd scan-pdf-to-modulusbarn
   ```

2. **Ensure Dependencies are Installed**:
   Install required libraries (see [Prerequisites](#prerequisites)).

3. **Configure**:
   - Add your private key file (`privatekey.pem`) to the project directory.
   - Change variables to your environment-details at the top of token_handler.py and main-py

4. **Run the Script**:
   Run the `main.py` script:
   ```bash
   python main.py
   ```

5. **Monitor Logs**:
   Check the `log/` folder for logs of successful uploads.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
