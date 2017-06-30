#!/usr/bin/python3
import sys
import os
import time
import re
import collections
import string
import psycopg2
sys.path.append('/home/art/work_stuff/pykick/lib')
from kicker_lib import *

#
# MAIN
#

if __name__ == '__main__':

    configfile = '/home/art/work_stuff/pykick/config/kickstart.config'
    logfile = '/home/art/work_stuff/pykick/logs/dbupdater.log'
    ks_parms = {}
    global_info = {}
    network_info = collections.defaultdict(dict)
    network_v6_info = collections.defaultdict(dict)
    server_info = collections.defaultdict(dict)
    dbconn = ''
    dbconn_list = ''
    ksfile = ''
 
    if len(sys.argv) != 2:
        print('Usage: dbupater.py <CONFIG FILE>')
        raise SystemExit(1)
    ksfile = str(sys.argv[1])
    if not os.path.exists(ksfile):
        print('config file ',ksfile,' is broken.... Usage: dbupdater.py <CONFIG FILE>')
        raise SystemExit(1)
    ret = os.path.exists(configfile)
    if ret:
        start_logging(logfile)
        get_ks_parms(configfile,ks_parms)
        dbconn = open_db(ks_parms)
        dbconn_list = open_list_db(ks_parms)
        read_config_file(dbconn,ksfile,global_info,network_info,network_v6_info,server_info)
        print_config_info(global_info,network_info,network_v6_info,server_info)
        update_global_db(dbconn,dbconn_list,global_info)
        update_network_db(dbconn,global_info,network_info)
        update_network_v6_db(dbconn,global_info,network_v6_info)
        update_server_db(dbconn,global_info,server_info)
        close_db(dbconn)
        print('dbupater completed on config file ',ksfile)
        raise SystemExit(1)
    else:
        print('Configfile [',configfile,'] missing....so exit')
        raise SystemExit(1)
