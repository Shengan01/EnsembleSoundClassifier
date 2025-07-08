# Use the official CUDA 12.2 base image
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Set the working directory
WORKDIR /instrument_classifier

# Install Miniconda
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Add Miniconda to the PATH
ENV PATH /opt/conda/bin:$PATH

# Create a new conda environment and install the required packages (excluding tensorflow/keras)
RUN conda create -n myenv -y -c conda-forge \
    python=3.9.19 \
    jupyter=1.1.1 \
    librosa=0.11.0 \
    python-dotenv=1.0.1 \
    psycopg2=2.9.9 \
    numpy=1.22.4 \
    pandas=2.2.3 \
    matplotlib=3.8.4 \
    seaborn=0.13.2 \
    ipykernel=6.29.5 \
    scikit-learn=1.3.0 \
    joblib=1.3.0 \
    tqdm=4.67.1 \
    scipy=1.16.0 \
    && conda clean --all -f -y

# Activate the conda environment and ensure it is used with Jupyter Notebook
RUN echo "source activate myenv" > ~/.bashrc
ENV PATH /opt/conda/envs/myenv/bin:$PATH

# Install TensorFlow 2.15 and Keras 2.15 with pip (for CUDA 12.x support)
RUN /opt/conda/envs/myenv/bin/pip install --upgrade pip && \
    /opt/conda/envs/myenv/bin/pip install tensorflow==2.15 keras==2.15

# Expose the Jupyter Notebook port
EXPOSE 8888

# Start Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]