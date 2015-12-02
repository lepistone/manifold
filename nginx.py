from flask import render_template


class NginxConfigRenderer():

    def __init__(self, manifold):
        self.manifold = manifold
        self.app = manifold.app
        self.dock = manifold.dock

    def render(self, minions):
        with self.app.app_context():
            return render_template('nginx.conf',
                                   manifold=self.manifold,
                                   minions=minions)

    def write(self, minions):
        content = self.render(minions)
        conf_path = self.manifold.config.NGINX_CONF_PATH
        with open(conf_path, 'w') as f:
            f.write(content)
