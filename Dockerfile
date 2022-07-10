FROM python:3.8.6-slim-buster

# set working directory in container
WORKDIR /usr

# Copy and install packages
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# Copy app folder to app folder in container
COPY /src/ /usr/src/
COPY /model/ /usr/model/

# Changing to non-root user
RUN useradd -m appUser
USER appUser

# Run locally
CMD gunicorn src.app.app:server -b:8000 --timeout 120