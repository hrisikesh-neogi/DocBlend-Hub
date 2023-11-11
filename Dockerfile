# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port that Streamlit will run on
EXPOSE 8501

# Define environment variable
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Run app.py when the container launches
CMD ["streamlit", "run", "home.py"]
