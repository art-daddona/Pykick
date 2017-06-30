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


def setup_openstack(global_info,server_info):
    import glob
    from shutil import copyfile
    import fileinput

    http_server_ip = global_info['HTTP_IP']
    scripts_http_location = 'http://' + http_server_ip + '/' + global_info['HTTP_TOP'] + '/openstack'
    os_path = global_info['OS_PATH']
    templates_path = global_info['TEMPLATES_PATH']
    openstack_path = global_info['OPENSTACK_PATH']
    os.chdir(openstack_path)
    openstack_files = glob.glob('*.yaml') 

    for filename in openstack_files:
        if os.path.isfile(filename):
            logging.info('setup_openstack unlink %s/%s',openstack_path,filename)
            os.unlink(filename)

    server_list = []
    for key in server_info:
        for subkey in server_info[key]:
            if subkey == 'HOSTNAME':
                server = server_info[key][subkey]
                server_list.append(server)

    for server in server_list:
        if server_info[server]['SYSTEM_TYPE'] == 'OPENSTACK':
            logging.info('setup_openstack start processing server=[%s]',server)
            heat_yaml_file = openstack_path + '/' + server + '-heat.yaml'
            env_yaml_file = openstack_path + '/' + server + '-env.yaml'
            copyfile(templates_path + '/template-heat.yaml',heat_yaml_file)
            copyfile(templates_path + '/template-env.yaml',env_yaml_file)
            for line in fileinput.input(heat_yaml_file,inplace=1):
                if re.search('##DEFAULT_USER_PW##',line):
                    line = re.sub('##DEFAULT_USER_PW##',global_info['DEFAULT_USER_PW'],line)
                if re.search('##DEFAULT_USER##',line):
                    line = re.sub('##DEFAULT_USER##',global_info['DEFAULT_USER'],line)
                print(line,end='')
            for line in fileinput.input(env_yaml_file,inplace=1):
                if re.search('##HOSTNAME##',line):
                    line = re.sub('##HOSTNAME##',server,line)
                if re.search('##OPENSTACK_IMAGE##',line):
                    line = re.sub('##OPENSTACK_IMAGE##',server_info[server]['OPENSTACK_IMAGE'],line)
                if re.search('##OPENSTACK_FLAVOR##',line):
                    line = re.sub('##OPENSTACK_FLAVOR##',server_info[server]['OPENSTACK_FLAVOR'],line)
                if re.search('##OPENSTACK_MANAGEMENT_NETWORK##',line):
                    line = re.sub('##OPENSTACK_MANAGEMENT_NETWORK##',server_info[server]['OPENSTACK_MANAGEMENT_NETWORK'],line)
                if re.search('##MANAGEMENT_IP_V4##',line):
                    line = re.sub('##MANAGEMENT_IP_V4##',server_info[server]['MANAGEMENT_IP_V4'],line)
                if re.search('##OPENSTACK_APPLICATION_NETWORK##',line):
                    line = re.sub('##OPENSTACK_APPLICATION_NETWORK##',server_info[server]['OPENSTACK_APPLICATION_NETWORK'],line)
                if re.search('##APPLICATION_IP_V4##',line):
                    line = re.sub('##APPLICATION_IP_V4##',server_info[server]['APPLICATION_IP_V4'],line)
                if re.search('##OPENSTACK_SSH_KEY##',line):
                    line = re.sub('##OPENSTACK_SSH_KEY##',server_info[server]['OPENSTACK_SSH_KEY'],line)
                if re.search('##OPENSTACK_SECURITY_GROUP##',line):
                    line = re.sub('##OPENSTACK_SECURITY_GROUP##',server_info[server]['OPENSTACK_SECURITY_GROUP'],line)
                if re.search('##OPENSTACK_ZONE##',line):
                    line = re.sub('##OPENSTACK_ZONE##',server_info[server]['OPENSTACK_ZONE'],line)
                print(line,end='')
        logging.info('setup_openstack completed')


#
# MAIN
#

if __name__ == '__main__':
    configfile = '/home/art/work_stuff/pykick/config/kickstart.config'
    logfile = '/home/art/work_stuff/pykick/logs/openstack-create.log'
    ks_parms = {}
    configname = ''
    global_info = {}
    server_info = collections.defaultdict(dict)

    if len(sys.argv) != 2:
        print('Usage: openstack-create.py <GLOBAL_NAME>')
        raise SystemExit(1)
    start_logging(logfile)
    get_ks_parms(configfile,ks_parms)
    dbconn = open_db(ks_parms)

    configname = str(sys.argv[1])
    global_fk = get_global_fk(dbconn,configname)
    if global_fk:
        logging.info('global name [%s] good....so continue',configname)
        read_db_config(dbconn,global_fk,global_info,server_info)
        setup_openstack(global_info,server_info)
        print('openstack-create.py has completed. Logfile is ',logfile)
        raise SystemExit(1)
    else:
        logging.info('Config Name [%s] invalid....so exit',configname)
        print('Config Name [',configname,'] invalid....so exit')
        raise SystemExit(1)
