FROM python:3.7

WORKDIR /mycloud

ENV MYCLOUD_DOCKER=1

RUN pip install keyrings.cryptfile

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

RUN apt-get update && apt-get install -y chromium=80.0.3987.162-1~deb10u1
RUN wget https://chromedriver.storage.googleapis.com/80.0.3987.16/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver

RUN apt-get install -y gnome-keyring

COPY ./ ./

RUN python setup.py install

ENTRYPOINT ["/bin/bash"]
