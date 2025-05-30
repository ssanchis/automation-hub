# Automation Hub – Report Downloader

This script uses Selenium to automate the download of reports or files from a web page.

## Script 1: `download_reports.py`

### What it does
Automates browser interaction to:
1. Open a webpage
2. Locate a download button by its HTML ID
3. Click it
4. Wait for the file to download

### Requirements
- Google Chrome installed
- Python 3.7+
- Dependencies:
  ```bash
  pip install selenium webdriver-manager

