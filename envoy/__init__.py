# Import the version number at the top level
from .version import get_version, __version_info__

__version__ = get_version(short=True)
