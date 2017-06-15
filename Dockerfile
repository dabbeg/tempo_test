FROM python:3.4-alpine
COPY ./requirements.txt /code/
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
