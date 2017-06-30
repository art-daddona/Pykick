#!/usr/bin/python3
import sys
import os
import time
import logging
import re
import collections
import psycopg2




def exit_error(err_buffer):
    logging.info('ERROR:[%s] Exit',err_buffer)
    print('ERROR:[',err_buffer,'] Exit')
    raise SystemExit(1)

def start_logging():
    logging.basicConfig(filename=logfile,filemode='w',level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info('logging started')

def open_db(ks_parms):
    dbhost = ks_parms['IP']
    dbport = ks_parms['PORT']
    dbname = ks_parms['DB']
    dbuser = ks_parms['USER']
    dbpass = ks_parms['PASS']
    dbconn = psycopg2.connect(database=dbname,user=dbuser,password=dbpass,host=dbhost,port=dbport)
    logging.info('open_db completed')
    return(dbconn)

def close_db(dbconn):
    dbconn.close()
    logging.info('close_db completed')

def get_ks_parms(ks_parms,configfile):
    fh = open(configfile,'rt')
    for line in fh:
        line = line.rstrip('\n')
        line = line.rstrip('\r')
        if not line.startswith('#'):
            attr,value = line.split('=')
            ks_parms[attr] = value
            logging.info('get_ks_parms [%s] = [%s]',attr,value)
    fh.close()
    logging.info('get_ks_parms completed')

def get_global_fk(configname):
    sql = 'SELECT global_fk FROM globals WHERE global_name = %s;'
    sql_data = (configname,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    curret = cur.fetchone()
    if not curret:
        global_fk = 0
    else:
        global_fk = curret[0]
        logging.info('get_global_fk completed %s',global_fk)
    cur.close()
    return(global_fk)

#
#START read_config
#
def read_config(dbconn,global_fk,global_info,server_info):
    global_name = ''
    server_name = ''

    sql = 'SELECT global_name,dhcpd_ip,dhcpd_path,tftpd_ip,tftpd_path,http_ip,http_top,os_path,scripts_path,templates_path,software_path,vm_path,openstack_path,keyboard,timezone,root_pw,default_user,default_user_pw,dns_servers,ntp_servers,domain,search_domains,log_server,nagios_server from globals WHERE global_fk= %s;'
    sql_data = (global_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    rows = cur.fetchone()
    cur.close()
    if not len(rows):
        out_buffer = 'ERROR reading database table globals for gobal_fk [' + global_fk + ']'
        print(out_buffer)
        return(0)
    global_info['GLOBAL_NAME'],global_info['DHCPD_IP'],global_info['DHCPD_PATH'],global_info['TFTPD_IP'],global_info['TFTPD_PATH'],global_info['HTTP_IP'],global_info['HTTP_TOP'],global_info['OS_PATH'],global_info['SCRIPTS_PATH'],global_info['TEMPLATES_PATH'],global_info['SOFTWARE_PATH'],global_info['VM_PATH'],global_info['OPENSTACK__PATH'],global_info['KEYBOARD'],global_info['TIMEZONE'],global_info['ROOT_PW'],global_info['DEFAULT_USER'],global_info['DEFAULT_USER_PW'],global_info['DNS_SERVERS'],global_info['NTP_SERVERS'],global_info['DOMAIN'],global_info['SEARCH_DOMAINS'],global_info['LOG_SERVER'],global_info['NAGIOS_SERVER'] = rows

    sql = 'SELECT server_fk,hostname,os_version,drive,swap,console_port,console_speed,pxe_mac,pxe_device,management_device,management_ip_v4,management_ip_v6,application_device,application_ip_v4,application_ip_v6,system_type,application_type,domain,status from servers WHERE global_fk= %s AND system_type = %s;'
    sql_data = (global_fk,'VBOX',)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    rows = cur.fetchall()
    cur.close()
    if not len(rows):
        out_buffer = 'ERROR reading database table servers for gobal_fk [' + global_fk + ']'
        print(out_buffer)
        return(0)
    for row in rows:
        key = row[1]
        server = key
        server_fk,server_info[key]['HOSTNAME'],server_info[key]['OS_VERSION'],server_info[key]['DRIVE'],server_info[key]['SWAPSIZE'],server_info[key]['CONSOLE_PORT'],server_info[key]['CONSOLE_SPEED'],server_info[key]['PXE_MAC'],server_info[key]['PXE_DEVICE'],server_info[key]['MANAGEMENT_DEVICE'],server_info[key]['MANAGEMENT_IP_V4'],server_info[key]['MANAGEMENT_IP_V6'],server_info[key]['APPLICATION_DEVICE'],server_info[key]['APPLICATION_IP_V4'],server_info[key]['APPLICATION_IP_V6'],server_info[key]['SYSTEM_TYPE'],server_info[key]['APPLICATION_TYPE'],server_info[key]['DOMAIN'],server_info[key]['STATUS'] = row
        sql = 'SELECT vm_type,vm_host,vm_rdp_port,vm_memory,vm_cpu,vm_interface_device,vm_drive_type,vm_iscsi_target,vm_iscsi_port,vm_iscsi_iqn from vm_info WHERE global_fk = %s AND server_fk = %s;'
        sql_data = (global_fk,server_fk,)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        rows = cur.fetchone()
        cur.close()
        if not len(rows):
            out_buffer = 'ERROR reading database table vm_info for server [' + server + ']'
            print(out_buffer)
        server_info[server]['VM_TYPE'],server_info[server]['VM_HOST'],server_info[server]['VM_RDP_PORT'],server_info[server]['VM_MEMORY'],server_info[server]['VM_CPU'],server_info[server]['VM_INTERFACE_DEVICE'],server_info[server]['VM_DRIVE_TYPE'],server_info[server]['VM_ISCSI_TARGET'],server_info[server]['VM_ISCSI_PORT'],server_info[server]['VM_ISCSI_IQN'] = rows
    return(1)
#
#END read_config
#

#
#START setup_vbox
#   
def setup_vbox(global_info,server_info,ksparms):
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
    ksconfigfile = '/home/art/work_stuff/pykick/config/kickstart.config'
    logfile = '/home/art/work_stuff/pykick/logs/vbox-create.log'
    ksparms = {}
    configname = ''
    global_info = {}
    server_info = collections.defaultdict(dict)

    if len(sys.argv) != 2:
        print('Usage: vbox-create.py3 <GLOBAL_NAME>')
        raise SystemExit(1)
    start_logging()
    get_ks_parms(ksparms,ksconfigfile)
    dbconn = open_db(ksparms)

    configname = str(sys.argv[1])
    global_fk = get_global_fk(configname)
    if global_fk:
        logging.info('global name [%s] good....so continue',configname)
        read_config(dbconn,global_fk,global_info,server_info)
        setup_vbox(global_info,server_info,ksparms)
        print('vbox-create.py has completed. Logfile is ',logfile)
        raise SystemExit(1)
    else:
        logging.info('Config Name [%s] invalid....so exit',configname)
        print('Config Name [',configname,'] invalid....so exit')
        raise SystemExit(1)
