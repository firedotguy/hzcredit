from logging import basicConfig, getLogger, WARNING
from sysconfig import get_paths
from site import getsitepackages, getusersitepackages

from rich.logging import RichHandler
from rich.traceback import install

stdlib = get_paths()["stdlib"]
site_pkgs = []
try:
    site_pkgs += getsitepackages()
except Exception:
    pass
usp = getusersitepackages()
if usp:
    site_pkgs.append(usp)

install(width=200, code_width=120, theme='monokai', show_locals=True, suppress=[stdlib, *site_pkgs], locals_max_length=2, locals_max_string=80)
basicConfig(
    level='DEBUG', format='%(message)s', handlers=[RichHandler(
        rich_tracebacks=True, tracebacks_width=200, tracebacks_code_width=120, tracebacks_show_locals=True, tracebacks_theme='monokai',
        tracebacks_suppress=[stdlib, *site_pkgs], locals_max_length=2, locals_max_string=80
    )]
)
getLogger('aiogram.dispatcher').setLevel(WARNING)
getLogger('aiogram.event').setLevel(WARNING)
getLogger('asyncio').setLevel(WARNING)


def get_logger():
    return getLogger()