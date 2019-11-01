FROM python:3.7

ENV APP_HOME /app
WORKDIR $APP_HOME

#RUN apk add libreoffice build-base msttcorefonts-installer fontconfig && update-ms-fonts && fc-cache -f

RUN pip install Pillow
RUN pip install Flask requests gevent 
RUN pip install google-cloud-storage

RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin

COPY . $APP_HOME

# prevent libreoffice from querying ::1 (ipv6 ::1 is rejected until istio 1.1)
#RUN mkdir -p /etc/cups && echo "ServerName 127.0.0.1" > /etc/cups/client.conf

CMD ["python", "crop.py"]
