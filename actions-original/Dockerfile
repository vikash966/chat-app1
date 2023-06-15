FROM rasa/rasa-sdk:latest

USER root
WORKDIR /app

#USER root

COPY ./actions /app/actions

COPY req.txt /app

#COPY ./database_utils /app/database_utils

RUN pip3 install -r req.txt

CMD ["start", "--actions", "actions"]

USER 1001
