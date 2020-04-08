FROM python:3.7
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "--workers=1", "--threads=1", "wsgi"]
