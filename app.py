from flask import Flask, Response, render_template, redirect, url_for
from docker import Client
from docker.utils import kwargs_from_env, create_host_config

import config
from util import pretty_json


app = Flask(__name__)
app.debug = True
doc = Client(**kwargs_from_env())
host_config = create_host_config(
    publish_all_ports=True,
)


@app.route('/all')
def all_containers():
    containers = doc.containers(trunc=True, all=True)
    return render_template('containers.html', containers=containers)


@app.route('/')
def containers():
    containers = doc.containers(trunc=True)
    return render_template('containers.html', containers=containers)


@app.route('/container/<cont_id>/start')
def start(cont_id):
    doc.start(container=cont_id)
    return redirect(url_for('containers'))


@app.route('/container/<cont_id>/login')
def login(cont_id):
    inspect = doc.inspect_container(container=cont_id)
    ext_port = list(inspect['NetworkSettings']['Ports'].values())[0][0]
    return redirect('http://{HostIp}:{HostPort}'.format(**ext_port))


@app.route('/pull')
def pull():
    def gen():
        yield b'Pulling image. Please wait! (streaming)\n'
        for line in doc.pull(config.repo, stream=True):
            yield pretty_json(line)
    return Response(gen())


@app.route('/new')
def new():
    doc.create_container(image=config.image, host_config=host_config)
    return redirect(url_for('containers'))


if __name__ == '__main__':
    app.run()
