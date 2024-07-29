FROM python:3.11-alpine

# Update and install packages
RUN apk update && apk upgrade && \
    apk add --no-cache bash build-base libffi-dev postgresql-dev

# Create a user and home directory
RUN adduser -D -u 1000 hbnb

# Switch to the hbnb user and move to the /home/hbnb directory
USER hbnb
WORKDIR /home/hbnb

# Create the data directory in the user's directory
RUN mkdir hbnb_data

# Copy Python dependencies from requirements.txt file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files into the container
COPY app ./app

# Define the Docker named volume "hbnb_data"
VOLUME ["/home/hbnb/hbnb_data"]

# Copy data files into the container
COPY --chown=hbnb:hbnb app/data/* /home/hbnb/hbnb_data/

# Set permissions on the mounted volume
RUN chmod -R 774 /home/hbnb/hbnb_data

# Define environment variable for the port and exposes it
ENV PORT 5000
EXPOSE 5000

# Define the entry point of the application
WORKDIR /home/hbnb/

CMD ["python", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
