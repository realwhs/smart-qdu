import sae
from smart_qdu import wsgi

application = sae.create_wsgi_app(wsgi.application)

