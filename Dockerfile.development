# Use PyTorch base image with CUDA 12.4 support
FROM nvcr.io/nvidia/pytorch:23.12-py3

# Set up the working directory
WORKDIR /workspace

# Install Python dependencies
COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install system tools (if needed)
RUN apt-get update && apt-get install -y \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Expose ports for VSCode
EXPOSE 3000