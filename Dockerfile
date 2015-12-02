FROM python

COPY . /app
RUN pip install -r /app/requirements.txt

WORKDIR /app
ENTRYPOINT ["python", "app.py"]
CMD [""]
