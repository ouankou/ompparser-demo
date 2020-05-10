
# Pull base image.
FROM ubuntu:20.04

# Add user
RUN groupadd -g 9999 dev && \
    useradd -r -u 9999 -g dev -m -d /home/dev dev

# Install packages.
RUN \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y \
        git \
        python3-flask \
        python3-requests \
        npm \
        vim \
        wget && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/*

RUN npm install serve -g

# Switch user and working directory.
USER rose
COPY --chown=dev:dev [".bashrc", "/home/dev/"]
COPY --chown=dev:dev ["frontend", "/home/dev/frontend"]
COPY --chown=dev:dev ["flask", "/home/dev/flask"]

WORKDIR /home/dev
RUN git clone -b dev https://github.com/passlab/ompparser.git && \
    cd ompparser && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=../../ompparser_install .. && \
    make && \
    make install

ENV PATH /home/dev/ompparser_install

WORKDIR /home/dev/frontend
RUN npm ci && \
    npm run build

# Define default command.
CMD ["serve", "-s", "build"]
