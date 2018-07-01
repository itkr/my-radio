FROM ubuntu:18.04
MAINTAINER itkr itkrst@gmail.com
LABEL title="my-radio"
LABEL description="Play radio with Google Chrome and radio.jp"

ENV TZ "Asia/Tokyo"

RUN apt update -y
# RUN apt install -y python3-dev python3-pip
RUN apt install -y python-dev python-pip

ARG PROJECT_PATH=/root
WORKDIR ${PROJECT_PATH}
COPY . ${PROJECT_PATH}/

# apt install wget
# apt install gnupg
# sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
# wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# apt update
# apt install google-chrome-stable

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "play.py"]
# CMD ["-V"]