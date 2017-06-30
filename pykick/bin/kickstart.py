#!/usr/bin/python3
import sys
import os
import time
import logging
import re
import collections
import psycopg2
sys.path.append('/home/art/work_stuff/pykick/lib')
from kicker_lib import *

#
# MAIN
#
if __name__ == '__main__':
    configfile = '/home/art/work_stuff/pykick/config/kickstart.config'
    logfile = '/home/art/work_stuff/pykick/logs/kickstart.log'
    ks_parms = {}
    configname = ''
    global_info = {}
    network_info = collections.defaultdict(dict)
    network_v6_info = collections.defaultdict(dict)
    server_info = collections.defaultdict(dict)
    if len(sys.argv) != 2:
        print('Usage: kickstart.py <GLOBAL_NAME>')
        raise SystemExit(1)
    start_logging(logfile)
    get_ks_parms(configfile,ks_parms)
    dbconn = open_db(ks_parms)
    configname = str(sys.argv[1])
    global_fk = get_global_fk(dbconn,configname)
    if global_fk:
        logging.info('global name [%s] good....so continue',configname)
        read_db_config(dbconn,global_fk,global_info,server_info)
        read_db_network_config(dbconn,global_fk,network_info,network_v6_info)
        print_config_info(global_info,network_info,network_v6_info,server_info)
        check_server_network(global_info,server_info,network_info,network_v6_info)
        setup_dhcp(global_info,network_info,ks_parms)
        setup_tftpd(global_info,ks_parms)
        setup_servers(global_info,network_info,server_info,ks_parms)
        setup_servers_info(global_info,server_info)
        setup_servers_scripts(global_info,server_info,network_info,network_v6_info)
        restart_dhcp(ks_parms,global_info)
        print('kickstart.py has completed. Logfile is ',logfile)
        raise SystemExit(1)
    else:
        logging.info('Config Name [%s] invalid....so exit',configname)
        print('Config Name [',configname,'] invalid....so exit')
        raise SystemExit(1)
