ARG PYTHON_IMAGE

FROM ${PYTHON_IMAGE}

RUN apt update

RUN apt install --yes apt-transport-https ca-certificates wget dirmngr gnupg software-properties-common

RUN wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add -

RUN add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/

RUN apt update

RUN apt install --yes adoptopenjdk-8-hotspot

WORKDIR /code/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --use-deprecated=legacy-resolver --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./sources /code/sources/

CMD ["streamlit", "run", "sources/main.py"]
