FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip 
RUN pip install  -r requirements.txt

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
