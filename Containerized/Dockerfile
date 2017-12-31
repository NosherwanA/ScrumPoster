FROM alpine:3.1
MAINTAINER nosherwan.a2@gmail.com

# Update and install app dependencies
RUN apk update
RUN apk add python py-pip
RUN pip install mattermostapi
RUN apk add bash

# Add necessary files 
COPY ScrumPoster.py /src/ScrumPoster.py
COPY ChannelAdd.py /src/ChannelAdd.py
COPY config/config.json /src/config/config.json
COPY scrum_list/scrum_list.json /src/scrum_list/scrum_list.json
ADD cronSchedule.txt /src/cronSchedule.txt

#Modify permissions for files and schedule cron jobs
RUN chmod 0644 /src/ScrumPoster.py /src/ChannelAdd.py /src/cronSchedule.txt /src/config/config.json /src/scrum_list/scrum_list.json
RUN /usr/bin/crontab /src/cronSchedule.txt

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
