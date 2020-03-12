# Official Python image
FROM python:3.7

# Set the working directory
WORKDIR /xapotest/api

# Copy project contents into the container at /xapotest/api
COPY . /xapotest/api

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose Port
EXPOSE 8080

# Run wsgi.py when the container launches
CMD ["python", "manage.py", "runserver"]