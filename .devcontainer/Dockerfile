# This Dockerfile sets up a development environment for my meccano project
# containing FreeCAD and additional tools.
ARG FreeCAD_VERSION
FROM lscr.io/linuxserver/freecad:${FreeCAD_VERSION}

RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    zsh \ 
    vim 
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

RUN pip3 install uv

COPY ./meccano /package/meccano
COPY ./pyproject.toml /package/

RUN /opt/freecad/usr/bin/python -m pip install /package