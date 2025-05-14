# For more information, please refer to https://aka.ms/vscode-docker-python
FROM ubuntu:22.04 AS base

# 设置非交互模式，避免安装过程中提示交互
ENV DEBIAN_FRONTEND=noninteractive

# 安装依赖库以及工具
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository "deb http://security.ubuntu.com/ubuntu focal-security main"
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    libnss3 \
    libxi6 \
    libgdk-pixbuf2.0-0 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxext6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxkbcommon-dev \
    libgbm-dev \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libasound2 \
    libasound2-data \
    libxfixes3 \
    libpangocairo-1.0-0 \
    libcups2 \
    libxshmfence1 \
    xfonts-utils \
    xfonts-encodings \
    fontconfig \
    fonts-dejavu-core \
    tzdata \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' > /etc/timezone \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "deb http://archive.ubuntu.com/ubuntu focal main universe" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    xfonts-75dpi \
    xfonts-base
    
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb && \
    apt-get install -y ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb || apt-get -f install -y && \
    rm -f ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /

# 克隆 Git 存储库
RUN git clone https://liguoqiang0121%40qq.com:Aa123456@gitee.com/lucasli0121/smart_school_web.git
WORKDIR /smart_school_web

RUN mkdir /usr/share/fonts/chinese && \
    cp /smart_school_web/static/fonts/* /usr/share/fonts/chinese/
RUN cd /usr/share/fonts/chinese && \
    fc-cache -f -v && \
    fc-list

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /smart_school_web
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["python3", "main.py"]
#CMD ["python", "main.py"]
