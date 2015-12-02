FROM python

COPY . /app
RUN pip install -r /app/requirements.txt

EXPOSE 5000
WORKDIR /app
ENTRYPOINT ["python", "app.py"]
CMD [""]
