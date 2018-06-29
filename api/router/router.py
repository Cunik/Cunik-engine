"""Route.
    /run POST
    /info/<id> GET
"""

from .route import Route
from .cunik import cunik_bp

routes = [
    Route(cunik_bp, '/cunik')
]
