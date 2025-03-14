FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    git wget curl unzip vim \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel

WORKDIR /workspace

COPY . .

RUN pip install -r requirements.txt

CMD ["bash", "-c", "python -c 'import torch; print(torch.__version__)' && python -c 'import torch; print(torch.version.cuda)'"]
