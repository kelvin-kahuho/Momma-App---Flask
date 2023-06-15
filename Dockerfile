#Use appropriate Python base image
FROM python:3.9-slim

#Set the working directory in the container
WORKDIR /app/Momma-app---FLASK

#Copy the all files

COPY . .

#install python dependecies in requirements.txt file to the container
RUN pip install --no-cache-dir -r requirements.txt

#Expose the port on which your flask app runs
EXPOSE 5000

#Set the environment variable for Flask
ENV FLASK_APP=run.py

# Run the Flask app using Gunicorn server
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:5000"]