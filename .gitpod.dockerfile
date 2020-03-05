FROM gitpod/workspace-mysql

# install linux requirements
USER root
RUN apt-get update && apt-get upgrade && apt-get install -y pkg-config python3.7-dev
