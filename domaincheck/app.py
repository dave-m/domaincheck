"""
Domain checker
Shows a website that allows you to check the status of a domain
"""
import os
from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest
from check import full_search
from pulsar.apps import wsgi

app = Flask(__name__)

@app.route('/')
def main():
    """Main index page

    """
    return render_template('index.html')

@app.route('/check/<domain_name>', methods=['GET'])
def check_domain(domain_name):
    """Accept POST, check domain details for supplied
    domain

    """
    if not domain_name:
        return BadRequest('No supplied domain!')

    res = full_search(domain_name)

    if not res['a'] and not res['mx'] and not res['nameservers']:
        return NotFound('No data for domain: {0}'.format(domain_name))

    res['a'] = [(a[0]+domain_name, a[1]) for a in res['a']]

    return jsonify(res)


class Wsgi(wsgi.LazyWsgi):
    """WSGI Wrapper around our app to interop with pulsar

    """

    def setup(self):
        """Return back a handler for our app that will include
        the :wsgi:`wait_for_body_middleware`

        """
        return wsgi.WsgiHandler((wsgi.wait_for_body_middleware, app))

def server(name, **kwargs):
    """Generate WSGI server

    """
    app.debug = kwargs.get('debug') or False
    return wsgi.WSGIServer(Wsgi(), name=name, **kwargs)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    server('domaincheck-wsgi', bind='0.0.0.0:{0}'.format(port)).start()
