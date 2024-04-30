# Use the Miniconda base image for Python 3.12
FROM continuumio/miniconda3:latest

# Set the working directory in the container
WORKDIR /app

# Copy the Conda environment file to the working directory
COPY environment.yml .

# Create and activate the Conda environment
RUN conda env create -f environment.yml &&
    echo "source activate myenv" >~/.bashrc

# Make RUN, CMD, and ENTRYPOINT commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port your app runs on
EXPOSE 8080

# Specify the command to run your application
CMD ["python", "app.py"]
