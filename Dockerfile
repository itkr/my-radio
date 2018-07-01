FROM ubuntu:18.04
MAINTAINER itkr itkrst@gmail.com
LABEL title="my-radio"
LABEL description="Play radio with Google Chrome and radio.jp"

# 環境変数

ENV TZ "Asia/Tokyo"
ENV PYTHONIOENCODING "utf-8"

# 依存モジュールインストール

RUN apt update -y
RUN apt install -y python3-dev python3-pip wget unzip gnupg
# RUN apt install -y python-dev python-pip wget unzip gnupg

# コードコピー

ARG PROJECT_PATH=/root
WORKDIR ${PROJECT_PATH}
COPY . ${PROJECT_PATH}/

# Google Chrome インストール

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt update -y
RUN apt install -y google-chrome-stable

# Seleniumのドライバ取得

RUN wget https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip

# Pythonライブラリ

RUN pip3 install -r requirements.txt
# RUN pip install -r requirements.txt

# 実行コマンド

ENTRYPOINT ["python3", "play.py"]
# ENTRYPOINT ["python", "play.py"]

# CMD ["-V"]