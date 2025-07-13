FROM ubuntu:latest

USER root

# Install Python and Numpy
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  python3-dev \
  python3-pip \
  python3-setuptools \
  python3-wheel \
  python3-yaml \
  python3-typing-extensions \
  python3-numpy && \
  apt-get -y clean && \
  rm -rf /var/cache/apt /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install PyTorch dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    libopenblas-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libatlas-base-dev \
    gfortran \
    libffi-dev \
    wget cmake \
    gcc g++ make \
    libssl-dev && \
    apt-get -y clean && \
    rm -rf /var/cache/apt /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install PyTorch
ARG TORCH_VERSION=2.7.0
ARG TORCH_PLATFORM="cpu"
RUN zip_filename="libtorch-cxx11-abi-shared-with-deps-${TORCH_VERSION}%2B${TORCH_PLATFORM}.zip" && \
    wget --progress=dot:mega -O libtorch.zip \
        "https://download.pytorch.org/libtorch/${TORCH_PLATFORM}/${zip_filename}" && \
    unzip libtorch.zip && \
    mv libtorch /opt/pytorch && \
    rm -f libtorch.zip

# Install vAccel
RUN wget --progress=dot:mega \
        https://s3.nbfc.io/nbfc-assets/github/vaccel/rev/main/x86_64/release/vaccel_latest_amd64.deb && \
    apt install -y ./vaccel_latest_amd64.deb && \
    rm -f vaccel_latest_amd64.deb && \
    ldconfig

# Install vAccel RPC plugin
RUN wget --no-check-certificate --progress=dot:mega \
        https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/rpc/rev/main/x86_64/release/vaccel-rpc_latest_amd64.deb && \
    apt install -y ./vaccel-rpc_latest_amd64.deb  && \
    rm -f vaccel-rpc_latest_amd64.deb

RUN apt update && apt install -y pkg-config libcurl4-openssl-dev
COPY . /app
RUN mkdir -p build && \
    cd build && \
    cmake .. -DCMAKE_PREFIX_PATH=/opt/pytorch -DVACCEL=ON && \
    make

RUN mkdir -p build_stock && \
    cd build_stock && \
    cmake .. -DCMAKE_PREFIX_PATH=/opt/pytorch -DVACCEL=OFF && \
    make

RUN wget --progress=dot:mega https://s3.nbfc.io/torch/cnn_trace.pt

ENV VACCEL_PLUGINS=libvaccel-rpc.so
ENV VACCEL_LOG_LEVEL=4
ENV VACCEL_RPC_ADDRESS="unix:///var/run/vaccel/vaccel.sock"

