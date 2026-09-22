import sys
import logging

from kr8s.objects import new_class

from constants import TPS_CONSTS

PLUGINS = 'plugins'

class Console(new_class('Console', version='operator.openshift.io/v1', namespaced=False)):
    pass

console_cluster = Console.get('cluster')
plugin_list: list = console_cluster[TPS_CONSTS.SPEC][PLUGINS]
if (sys.argv[1] not in plugin_list):
    logging.info(f'adding plugin {sys.argv[1]} to operator.openshift.io/console cluster')
    plugin_list.append(sys.argv[1])
    console_cluster.patch({TPS_CONSTS.SPEC: {PLUGINS: plugin_list }}, type='merge')