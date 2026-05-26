from importlib.metadata import version

from .main import create_app

__version__ = version(__name__)

app = create_app()
