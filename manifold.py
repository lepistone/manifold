import socket
import docker
import config

from nginx import NginxConfigRenderer


class Manifold():

    def __init__(self, app, dock):
        self.app = app
        self.dock = dock
        self.config = config.ManifoldConfig

    def reload_nginx(self):
        try:
            # TODO: get the name of the container(s) with docker-compose:
            # docker-compose ps -q nginx
            self.dock.kill(self.config.NGINX_CONTAINER,
                           'SIGHUP')
        except docker.errors.APIError as err:
            # TODO logger
            # Nginx container is probably not running
            print('Could not reload nginx: {}'.format(err))

    def nginx_write_and_reload(self, renderer=NginxConfigRenderer):
        renderer = NginxConfigRenderer(self)
        renderer.write(self.minions())
        self.reload_nginx()

    def minion_by_id(self, cont_id):
        container = self.dock.inspect_container(container=cont_id)
        return Minion(self, container)

    def minions(self, trunc=True, all=False):
        containers = self.containers(trunc=trunc, all=all)
        return [Minion(self, container) for container in containers]

    def containers(self, trunc=True,  all=False):
        filters = {'ancestor': self.config.DOCKER_IMAGE}
        filters.update(self.config.DOCKER_FILTER)

        return self.dock.containers(
            trunc=trunc,
            all=all,
            filters=filters,
        )

    @property
    def hostname(self):
        return socket.gethostname()

    @property
    def port(self):
        return '5000'

    @property
    def subdomain(self):
        return self.config.SUBDOMAIN

    @property
    def nginx_server_name(self):
        return r'~^{}\..*$'.format(self.subdomain)


class Composition():
    """ A composition of minions """


class Minion():

    def __init__(self, manifold, container):
        self.app = manifold.app
        self.dock = manifold.dock
        self.manifold = manifold
        self.container = container
        self._inspect = None

    @property
    def inspect(self):
        if self._inspect is None:
            self._inspect = self.dock.inspect_container(
                container=self.container['Id']
            )
        return self._inspect

    @property
    def state(self):
        return self.inspect['State']['Status']

    @property
    def hostname(self):
        return self.container['Id'][:12]

    @property
    def subdomain(self):
        return '{}.{}'.format(self.hostname, self.manifold.subdomain)

    @property
    def nginx_server_name(self):
        return r'~^{}\.{}\..*$'.format(self.hostname, self.manifold.subdomain)

    # TODO: we could have several ports in one minion and we could have
    # several minion in one 'docker-compose'
    @property
    def port(self):
        return '8069'

    @property
    def ip(self):
        network = self.inspect.get('NetworkSettings', {})
        return network.get('IPAddress') or ''

    # FIXME: specific to Odoo, should have a way to map all ports with
    # a location
    @property
    def longpolling_port(self):
        port_info = self.dock.port(self.container['Id'], 8070)
        return port_info[0]['HostPort'] if port_info else ''

    def build_url(self):
        parts = (self.subdomain,
                 self.manifold.config.DOMAIN)
        # TODO: https
        return 'http://{}.{}'.format(*parts)
