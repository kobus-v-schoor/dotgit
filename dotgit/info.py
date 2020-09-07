from os.path import expanduser
import socket

__version__ = '2.2.0'
__author__ = 'Kobus van Schoor'
__author_email__ = 'v.schoor.kobus@gmail.com'
__url__ = 'https://github.com/kobus-v-schoor/dotgit'
__license__ = 'GNU General Public License v2 (GPLv2)'

home = expanduser('~')
hostname = socket.gethostname()
