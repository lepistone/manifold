from flask import Flask
from docker import Client
from docker.utils import kwargs_from_env


app = Flask(__name__)
app.debug = True
doc = Client(**kwargs_from_env())


@app.route('/')
def hello_world():
    return str(doc.containers())

if __name__ == '__main__':
    app.run()
