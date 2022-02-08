ARG PYTHON_IMAGE

FROM ${PYTHON_IMAGE}

WORKDIR /code/server/

COPY ./requirements.txt /code/server/requirements.txt

RUN pip install --use-deprecated=legacy-resolver --no-cache-dir --upgrade -r /code/server/requirements.txt

COPY ./app /code/server/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
