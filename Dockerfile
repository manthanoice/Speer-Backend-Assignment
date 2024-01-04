# Adding docker because well even I am too lazy to follow all the manual steps
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

WORKDIR /app/speer

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]