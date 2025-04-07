# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12.5 AS base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /
# 安装 Git
RUN apt-get update && apt-get install -y git
# 克隆 Git 存储库
RUN git clone https://liguoqiang0121%40qq.com:Aa123456@gitee.com/lucasli0121/smart_school_web.git
WORKDIR /smart_school_web

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /smart_school_web
USER appuser

FROM base AS dev_containers_target_stage

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["python", "main.py"]
#CMD ["python", "main.py"]
