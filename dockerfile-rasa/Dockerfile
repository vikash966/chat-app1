FROM rasa/rasa:3.5.7
#FROM python:3.10.7

#RUN pip3 install rasa
#RUN pip install sqlalchemy[asyncio]
WORKDIR  '/app'
COPY . /app
USER root

RUN  rasa train 

VOLUME /app/models


CMD [ "run","-m","/app/models","--enable-api","--cors","*","--debug", "--port", "5006", "--port", "5007", "--port", "5008"]


# Extend the official Rasa SDK image
#1.FROM rasa/rasa-sdk:latest

# Use subdirectory as working directory
#2.WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
#COPY actions/requirements-actions.txt ./

# Change back to root user to install dependencies
#3.USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
#RUN pip install -r requirements-actions.txt
#RUN pip install --upgrade pip
#RUN pip3 install sqlite3
# Copy actions folder to working directory
#5.COPY ./actions /app/actions

# By best practices, don't run the code with root user
#6.USER 1001

