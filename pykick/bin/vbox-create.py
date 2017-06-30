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
#START setup_vbox
#   
def setup_vbox(global_info,server_info):
    import glob
    from shutil import copyfile
    import fileinput

    http_server_ip = global_info['HTTP_IP']
    vm_http_location = 'http://' + http_server_ip + '/' + global_info['HTTP_TOP'] + '/vm'
    os_path = global_info['OS_PATH']
    templates_path = global_info['TEMPLATES_PATH']
    vm_path = global_info['VM_PATH']
    os.chdir(vm_path)
    vm_files = glob.glob('*') 

    for filename in vm_files:
        if os.path.isfile(filename):
            logging.info('setup_vbox unlink %s/%s',vm_path,filename)
            os.unlink(filename)

    server_list = []
    for key in server_info:
        for subkey in server_info[key]:
            if subkey == 'HOSTNAME':
                server = server_info[key][subkey]
                server_list.append(server)

    for server in server_list:
        if server_info[server]['SYSTEM_TYPE'] == 'VBOX':
            if 'ubuntu' in server_info[server]['OS_VERSION']:
                os_type = 'Ubuntu_64'
            else:
                os_type = 'RedHat_64'
            logging.info('setup_vbox start prcessing server=[%s]',server)
            if server_info[server]['VM_DRIVE_TYPE'] == 'ISCSI':
                vbox_file = vm_path + '/' + server + '-vm-iscsi.vbox'
                copyfile(templates_path + '/template-vm-iscsi',vbox_file)
            elif server_info[server]['VM_DRIVE_TYPE'] == 'VDI':
                vbox_file = vm_path + '/' + server + '-vm-vdi.vbox'
                copyfile(templates_path + '/template-vm-vdi',vbox_file)
            for line in fileinput.input(vbox_file,inplace=1):
                if re.search('##HOSTNAME##',line):
                    line = re.sub('##HOSTNAME##',server,line)
                if re.search('##OS_TYPE##',line):
                    line = re.sub('##OS_TYPE##',os_type,line)
                if re.search('##VM_ISCSI_TARGET##',line):
                    line = re.sub('##VM_ISCSI_TARGET##',server_info[server]['VM_ISCSI_TARGET'],line)
                if re.search('##VM_ISCSI_IQN##',line):
                    line = re.sub('##VM_ISCSI_IQN##',server_info[server]['VM_ISCSI_IQN'],line)
                if re.search('##VM_ISCSI_PORT##',line):
                    line = re.sub('##VM_ISCSI_PORT##',str(server_info[server]['VM_ISCSI_PORT']),line)
                if re.search('##VM_CPU##',line):
                    line = re.sub('##VM_CPU##',str(server_info[server]['VM_CPU']),line)
                if re.search('##VM_MEMORY##',line):
                    line = re.sub('##VM_MEMORY##',str(server_info[server]['VM_MEMORY']),line)
                if re.search('##VM_INTERFACE_DEVICE##',line):
                    line = re.sub('##VM_INTERFACE_DEVICE##',server_info[server]['VM_INTERFACE_DEVICE'],line)
                if re.search('##VM_RDP_PORT##',line):
                    line = re.sub('##VM_RDP_PORT##',str(server_info[server]['VM_RDP_PORT']),line)
                if re.search('##VM_MAC##',line):
                    line = re.sub('##VM_MAC##',server_info[server]['PXE_MAC'],line)
                print(line,end='')
    logging.info('setup_servers completed')

#
#END setup_servers
#   

#
# MAIN
#

if __name__ == '__main__':
    configfile = '/home/art/work_stuff/pykick/config/kickstart.config'
    logfile = '/home/art/work_stuff/pykick/logs/vbox-create.log'
    ks_parms = {}
    configname = ''
    global_info = {}
    server_info = collections.defaultdict(dict)

    if len(sys.argv) != 2:
        print('Usage: vbox-create.py <GLOBAL_NAME>')
        raise SystemExit(1)
    start_logging(logfile)
    get_ks_parms(configfile,ks_parms)
    dbconn = open_db(ks_parms)

    configname = str(sys.argv[1])
    global_fk = get_global_fk(dbconn,configname)
    if global_fk:
        logging.info('global name [%s] good....so continue',configname)
        read_db_config(dbconn,global_fk,global_info,server_info)
        setup_vbox(global_info,server_info)
        print('vbox-create.py has completed. Logfile is ',logfile)
        raise SystemExit(1)
    else:
        logging.info('Config Name [%s] invalid....so exit',configname)
        print('Config Name [',configname,'] invalid....so exit')
        raise SystemExit(1)
