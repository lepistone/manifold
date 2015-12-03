from flask import Flask, Response, render_template, redirect, url_for, flash
from docker import Client
from docker.utils import kwargs_from_env

import config
from util import pretty_json
from manifold import Manifold


app = Flask(__name__)
app.config.from_object(config.FlaskConfig)

doc = Client(**kwargs_from_env())
host_config = doc.create_host_config(
    publish_all_ports=True,
)

manifold = Manifold(app, doc)
manifold.nginx_write_and_reload()


@app.route('/all')
def all_containers():
    minions = manifold.minions(trunc=True, all=True)
    return render_template('containers.html', minions=minions)


@app.route('/')
def containers():
    minions = manifold.minions(trunc=True)
    return render_template('containers.html', minions=minions)


@app.route('/container/<cont_id>/start')
def start(cont_id):
    doc.start(container=cont_id)
    manifold.nginx_write_and_reload()
    return redirect(url_for('containers'))


@app.route('/container/<cont_id>/login')
def login(cont_id):
    minion = manifold.minion_by_id(cont_id)
    return redirect(minion.build_url())


@app.route('/container/<cont_id>/logs')
def logs(cont_id):
    return manifold.dock.logs(cont_id).decode('utf8').replace('\n', '<br/>')


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
    flash('New container created for image {}'.format(config.image))
    return redirect(url_for('containers'))


if __name__ == '__main__':
    # not accessible through docker if only local
    app.run(host='0.0.0.0')
