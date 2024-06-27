# Use an official Python runtime as a parent image
FROM python:3.11-slim

####
RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* ./

# COPY ./package[s] ./packages

RUN poetry install  --no-interaction --no-ansi --no-root

# Install wkhtmltopdf and list binaries, redirect path to wkhtmlpdf to install_log.txt
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/* \
    && echo "wkhtmltopdf installed at: $(which wkhtmltopdf)" > /app/install_log.txt 

COPY . /app

RUN poetry install --no-interaction --no-ansi

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Environment variable for wkhtmltopdf
ENV XDG_RUNTIME_DIR=/tmp

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]



####

# # Set the working directory in the container
# WORKDIR /app

# # Install wkhtmltopdf and list binaries, redirect path to wkhtmlpdf to install_log.txt
# RUN apt-get update && apt-get install -y \
#     wkhtmltopdf \
#     && rm -rf /var/lib/apt/lists/* \
#     && echo "wkhtmltopdf installed at: $(which wkhtmltopdf)" > /app/install_log.txt 

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt

# # Make port 8501 available to the world outside this container
# EXPOSE 8501

# # Environment variable for wkhtmltopdf
# ENV XDG_RUNTIME_DIR=/tmp

# # Run app.py when the container launches
# CMD ["streamlit", "run", "app.py"]

