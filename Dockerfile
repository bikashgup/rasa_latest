# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:1.10.1

# Use subdirectory as working directory
WORKDIR /app

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN apt update -y
RUN pip install --upgrade pip
RUN pip install pandas
RUN pip install ruamel.yaml
RUN pip install loguru
RUN pip install redis
RUN pip install elasticsearch
RUN pip install ordered-set



# Copy actions folder to working directory
COPY ./actions /app/actions

# Copy config file into app
COPY config-env.yml /app/
COPY config_parser.py /app/
# Copy any additional custom requirements, if necessary (uncomment next line)

COPY actions/data/ /app/actions/data
COPY actions/api/ /app/actions/api
COPY ./getstream.py /app/ 

RUN apt-get update -y
RUN apt-get install telnet -y
RUN apt-get install -y iputils-ping


CMD ["start", "--actions", "actions"]
ENV PYTHONUNBUFFERED=0

# By best practices, don't run the code with root user
USER 1001
ENV PYTHONUNBUFFERED=0
# ENV PYTHONPATH=$PYTHONPATH:app/
