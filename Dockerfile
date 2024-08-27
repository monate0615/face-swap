FROM ubuntu:20.04

COPY . .

# Install python 3.10 or more latent
RUN sudo apt remove python3
RUN sudo rm -r /usr/bin/python3
RUN sudo apt install python3.10 python3.10-venv python3.10-dev
RUN sudo ln -s python3.10 /usr/bin/python3
RUN sudo apt install python3-pip
RUN sudo apt-get -y install python-html5lib
RUN sudo apt install gcc
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# Install NVIDIDA driver and CUDA library
RUN sudo apt install ubuntu-drivers-common
RUN sudo ubuntu-drivers devices
RUN sudo apt install nvidia-driver-550
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin 
RUN sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
RUN wget https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda-repo-ubuntu2004-12-4-local_12.4.1-550.54.15-1_amd64.deb
RUN sudo dpkg -i cuda-repo-ubuntu2004-12-4-local_12.4.1-550.54.15-1_amd64.deb
RUN sudo cp /var/cuda-repo-ubuntu2004-12-4-local/cuda-*-keyring.gpg /usr/share/keyrings/
RUN sudo apt-get update
RUN sudo apt-get -y install cuda-toolkit-12-4
RUN sudo apt-get -y install cuda-drivers

# Install env
RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
RUN pip install -r requirements.txt

# Download model
RUN python -m huggingface-downloader/download

CMD ["python", "-m", "main"]