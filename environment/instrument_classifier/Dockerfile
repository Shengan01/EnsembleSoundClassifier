# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /InstrumentClassification

# Install Miniconda
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Add Miniconda to the PATH
ENV PATH /opt/conda/bin:$PATH

# Create a new conda environment and install the required packages
RUN conda create -n myenv -y -c conda-forge  python=3.9.19 librosa=0.10.2.post1 tensorflow=2.4.1  keras=2.4.3 numpy=1.22.4 pandas=2.2.3 ipykernel=6.29.5 django=4.2.17&&\
    conda clean --all -f -y


# Activate the conda environment and ensure it is used with Jupyter Notebook
RUN echo "source activate myenv" > ~/.bashrc
ENV PATH /opt/conda/envs/myenv/bin:$PATH

# Expose the Django development server port
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]