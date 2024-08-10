# Discord Promo Checker

![Discord Promo Checker](https://img.shields.io/badge/Discord-Promo%20Checker-brightgreen)

## Overview

The **Discord Promo Checker** is a Python tool designed to check the validity of Discord promo codes. It allows users to input a list of promo codes and checks their status (claimed, unclaimed, or invalid) using the Discord API. The tool supports proxy usage to prevent rate limiting and enhance anonymity during checks.

## Features

- **Multi-threaded Checking**: Check multiple promo codes simultaneously to save time.
- **Proxy Support**: Optionally use proxies to avoid rate limits imposed by the Discord API.
- **Logging**: All operations are logged in a dedicated log file for troubleshooting and analysis.
- **Output Files**: Results are saved to separate text files for claimed, unclaimed, and invalid promos.
- **User-Friendly Interface**: Color-coded output in the terminal for better readability.
- **Configurable Settings**: Easily adjust settings like the number of threads and file paths through a configuration file.

## Requirements

- Python 3.x
- Required Python packages:
  - `requests`
  - `colorama`
  
You can install the required packages using pip:

```bash
pip install requests colorama
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

## Prepare Configuration Files

Create a `promos.txt` file containing the promo codes you want to check, one per line.

(Optional) Create a `proxies.txt` file containing your proxies in the format `ip:port:user:password`, one per line.

## Run the Tool

```bash
python promo_checker.py
```

## View Results

The results will be saved in the `output` directory:
- `unclaimed_promos.txt`
- `claimed_promos.txt`
- `invalid_promos.txt`
- `checker.log` (for logs)

## Disclaimer

This tool is intended for educational purposes only. Use it responsibly and ensure that you comply with Discord's Terms of Service. The author is not responsible for any misuse or consequences arising from the use of this tool. Always respect the privacy and rights of others when using this software.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.
Make sure to join my discord server at https://discord.gg/darkeyes