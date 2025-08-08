# This Dockerfile sets up a development environment for my meccano project
# containing FreeCAD and additional tools.

FROM lscr.io/linuxserver/freecad:1.0.2

RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    zsh \ 
    vim 

RUN pip3 install uv