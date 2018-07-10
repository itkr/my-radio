# my-radio

## Installation (Get source code)

```bash
git clone git@github.com:itkr/my-radio.git
```

## Preparation

### Install Selenium

```bash
pip install -r requirements.txt
```

### Install Driver

https://www.seleniumhq.org/download/

#### e.g.

```bash
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_mac64.zip
unzip chromedriver_mac64.zip
```

## Play Radio

```bash
python play.py
```
