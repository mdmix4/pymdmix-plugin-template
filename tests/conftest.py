from contextlib import contextmanager
from tempfile import NamedTemporaryFile
import shlex
import sqlalchemy

from unittest.mock import patch

from pymdmix_core.parser import get_mdmix_parser
from pymdmix_core.plugin.base import PluginManager

your_plugin_name = 'plugin_template'


def get_plugin_manager():
    '''Check if plugin can be found by the pluging manager'''
    plugin_manager = PluginManager(get_mdmix_parser())
    plugin_manager.load_plugin(f"pymdmix_{your_plugin_name}")
    return plugin_manager


def run_command(command: str, plugin_manager: PluginManager = None):
    plugin_manager = plugin_manager if plugin_manager is not None else get_plugin_manager()
    args = plugin_manager.parser.parse_args(shlex.split(command))
    plugin_manager.plugins[your_plugin_name].run(args)


@contextmanager
def db_patch():
    try:
        tmpfile = NamedTemporaryFile()
        with patch(
            "pymdmix_core.plugin.crud.SQL_ENGINE",
            sqlalchemy.create_engine(f"sqlite:///{tmpfile.name}")
        ) as db_engine:
            yield db_engine
    finally:
        tmpfile.close()
