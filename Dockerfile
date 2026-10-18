FROM pytorch/pytorch:2.14.1-cuda12.6-cudnn9-devel
ARG DEBIAN_FRONTEND=noninteractive

# Node/npm setup
RUN apt-get update && apt-get install -y apt-utils
RUN apt-get install curl -y
RUN apt-get install npm -y
RUN npm install -g n
RUN n lts

# Task install
RUN curl -1sLf 'https://dl.cloudsmith.io/public/task/task/setup.deb.sh' | bash && apt install task -y

# Pre-commit
RUN apt-get install pipx -y
RUN pipx install pre-commit
RUN pipx ensurepath