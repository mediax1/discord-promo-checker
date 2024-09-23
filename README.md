# Discord Promo Checker 🚀

![Discord Promo Checker](https://img.shields.io/badge/Discord-Promo%20Checker-brightgreen)

The **Discord Promo Checker** is the **ultimate** tool for checking the validity of Discord promo codes efficiently and reliably. Powered by multi-threading, intelligent proxy management, and a user-friendly interface, this tool is designed to give you the **fastest** and most accurate results possible. With added features for proxy health monitoring, advanced error handling, and detailed logging, **this is the best promo checker you’ll ever need**.

## 💥 Why is This the Best Discord Promo Checker?

- **Blazing Fast**: Thanks to **multi-threading** and parallel proxy testing, it processes hundreds of promo codes in no time.
- **Proxy Resilience**: With advanced proxy failure handling, the tool can rotate through proxies and even cool them down after failures. Say goodbye to rate limits!
- **Detailed Results**: Generates **clean reports** for claimed, unclaimed, and invalid promo codes, making it easy to track your findings.
- **Automatic Proxy Health Check**: Proxies are validated before use to ensure you’re only using healthy ones, avoiding unnecessary errors.
- **Retry Mechanism**: Promo checks automatically retry on failures, ensuring maximum reliability.
- **Fully Configurable**: Customize everything from thread count to proxy files with ease.

## 🚀 Features

- **Multi-threaded Checking**: Check multiple promo codes simultaneously for rapid results.
- **Proxy Support with Health Monitoring**: Proxies are rotated, monitored for failures, and put on cooldown when needed.
- **Logging**: Detailed logs are created for all operations, so you can troubleshoot or analyze performance anytime.
- **Output Files**: Separate output files for unclaimed, claimed, and invalid promos, organized for easy review.
- **User-Friendly Terminal Output**: Color-coded output for quick reading in the terminal.
- **Configurable Settings**: Easily adjust settings like the number of threads and file paths through a configuration file.

## 🛠️ Requirements

- Python 3.x
- Required Python packages:
  - `requests`
  - `colorama`
  - `python-dateutil`

You can install the required packages using pip:

```bash
pip install requests colorama python-dateutil
```

## Usage

### Clone the Repository:

```bash
git clone https://github.com/mediax1/discord-promo-checker.git
cd discord-promo-checker
```

## Prepare Configuration Files:

Create a `config.json` file in the root directory with the following structure:

```json
{
  "promos_file": "promos.txt",
  "proxies_file": "proxies.txt",
  "num_threads": 5
}
```

### Create Promo & Proxy Files:

- **promos.txt**: This file should contain the promo codes you want to check, one per line.
- **proxies.txt** (optional): If you are using proxies, this file should contain proxies in the format `ip:port:user:password`, one per line.

### Run the Tool

```bash
python promo_checker.py
```

## View Results

The results will be saved in the `output` directory:

- `unclaimed_promos.txt`
- `claimed_promos.txt`
- `invalid_promos.txt`
- `checker.log` (for logs)

## ⚠️ Disclaimer

This tool is intended for **educational purposes only**. Use it responsibly and ensure that you comply with Discord's Terms of Service. The author is not responsible for any misuse or consequences arising from the use of this tool. Always respect the privacy and rights of others when using this software.

## 📜 License

This project is licensed under the **MIT License**.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.
Make sure to join my discord server at https://discord.gg/darkeyes
