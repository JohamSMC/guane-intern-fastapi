FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app/app
COPY ./prestart.sh /app/

# Update pip
RUN /usr/local/bin/python -m pip install --upgrade pip

# Requirements are installed
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
