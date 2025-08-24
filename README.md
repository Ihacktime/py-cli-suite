# Py CLI Suite

A comprehensive suite of command-line utilities written in Python.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ihacktime/py-cli-suite.git
   cd py-cli-suite

2. Install the package in development mode:
    pip install -e .

Configuration
For the email functionality, create a .env file in the root directory with your email credentials:

EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

Usage:
    suite --help


Available Commands

- suite convert - Currency conversion tools

- suite email - Email tools (send daily quotes)

- suite web - Web tools (scraping)

- suite media - Media tools (YouTube downloader)

- suite contacts - Contact management tools

Examples
Currency Conversion:
suite convert currency 100 USD EUR

Send Daily Quotes:
suite email send-quotes --csv-file recipients.csv --quotes-file quotes.txt

Web Scraping:
suite web scrape https://example.com --selector ".content" --output output.html

YouTube Downloader:
suite media youtube https://www.youtube.com/watch?v=example --quality 720p --output-path ./downloads

Contact Management:
suite contacts add "John Doe" "123-456-7890" --email "john@example.com"
suite contacts list

Contributing
Feel free to contribute by submitting issues or pull requests.

Licence
This project is open source and available under the MIT License.


### .env.example
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

