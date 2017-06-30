#!/usr/bin/python3
import sys
import os
import time
import logging
import re
import collections
import string
import psycopg2

def exit_error(err_buffer):
    logging.info('ERROR:[%s] Exit',err_buffer)
    print('ERROR:[',err_buffer,'] Exit')
    raise SystemExit(1)

def start_logging(logfile):
    logging.basicConfig(filename=logfile,filemode='w',level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info('logging started')

def get_ks_parms(ks_parms):
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

def print_global(dbconn,global_fk,globalname):
    sql = 'SELECT global_name,dhcpd_ip,dhcpd_path,tftpd_ip,tftpd_path,http_ip,http_top,os_path,scripts_path,templates_path,software_path,vm_path,openstack_path,keyboard,timezone,root_pw,default_user,default_user_pw,dns_servers,ntp_servers,domain,search_domains,log_server,nagios_server from globals WHERE global_fk= %s;'
    sql_data = (global_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    row = cur.fetchone()
    cur.close()
    if not len(row):
        out_buffer = 'ERROR reading database table globals ' + globalname + ' for global_fk [' + global_fk + ']'
        print(out_buffer)
        exit_error(out_buffer)
    global_name,dhcpd_ip,dhcpd_path,tftpd_ip,tftpd_path,http_ip,http_top,os_path,scripts_path,templates_path,software_path,vm_path,openstack_path,keyboard,timezone,root_pw,default_user,default_user_pw,dns_servers,ntp_servers,domain,search_domains,log_server,nagios_server = row

    out_buffer = '[global=' + global_name + ']\nDHCPD_IP=' + dhcpd_ip + '\nDHCPD_PATH=' + dhcpd_path  + '\nTFTPD_IP=' + tftpd_ip
    print(out_buffer)
    out_buffer = 'TFTPD_PATH = ' + tftpd_path + 'HTTP_IP=' + http_ip + '\nHTTP_TOP=' + http_top + '\nOS_PATH=' + os_path + '\nSCRIPTS_PATH=' + scripts_path
    print(out_buffer)
    out_buffer = 'TEMPLATES_PATH=' + templates_path + '\nSOFTWARE_PATH=' + software_path + '\nVM_PATH=' + vm_path + '\nOPENSTACK_PATH=' + openstack_path
    print(out_buffer)
    out_buffer = 'KEYBOARD=' + keyboard + '\nTIMEZONE=' + timezone + '\nROOT_PW=' + root_pw + '\nDEFAULT_USER=' + default_user
    print(out_buffer)
    out_buffer = 'DEFAULT_USER_PW=' + default_user_pw + '\nDNS_SERVERS=' + dns_servers + '\nNTP_SERVERS=' + ntp_servers
    print(out_buffer)
    out_buffer = 'DOMAIN=' + domain + '\nSEARCH_DOMAINS=' + search_domains + '\nLOG_SERVER=' + log_server
    print(out_buffer)
    out_buffer = 'NAGIOS_SERVER=' + nagios_server + '\n\n'
    print(out_buffer)
    logging.info('read_global completed')


def print_subnet(dbconn,global_fk,globalname):
    sql = 'SELECT subnet_name,subnet_description,subnet_network,subnet_netmask,subnet_router,subnet_dhcp from subnet_v4 WHERE global_fk= %s;'
    sql_data = (global_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    rows = cur.fetchall()
    cur.close()
    if not len(rows):
        out_buffer = 'ERROR reading database table subnet_v4 ' + globalname + ' for global_fk [' + global_fk + ']'
        print(out_buffer)
        exit_error(out_buffer)
    for row in rows:
        key = row[0]
        network_v4_name,description,network,netmask,router,dhcp  = row
        out_buffer = '[subnet_v4=' + network_v4_name + ']\nDESCRIPTION=' + description + '\nNETWORK=' + network 
        print(out_buffer,end='')
        out_buffer = '\nNETMASK=' + netmask + '\nROUTER=' + router + '\nDHCP=' + str(dhcp) + '\n'
        print(out_buffer)

    sql = 'SELECT subnet_name,subnet_description,subnet_network,subnet_netmask,subnet_router,subnet_dhcp from subnet_v6 WHERE global_fk= %s;'
    sql_data = (global_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    rows = cur.fetchall()
    cur.close()
    if not len(rows):
        out_buffer = 'ERROR reading database table subnet_v6 ' + globalname + ' for global_fk [' + global_fk + ']'
        print(out_buffer)
        exit_error(out_buffer)
    for row in rows:
        key = row[0]
        network_v6_name,description,network,netmask,router,dhcp  = row
        out_buffer = '[subnet_v6=' + network_v6_name + ']\nDESCRIPTION=' + description + '\nNETWORK=' + network 
        print(out_buffer,end='')
        out_buffer = '\nNETMASK=' + netmask + '\nROUTER=' + router + '\nDHCP=' + str(dhcp) + '\n'
        print(out_buffer)

def print_server(dbconn,global_fk,globalname):
    sql = 'SELECT server_fk,hostname,os_version,drive,swap,console_port,console_speed,pxe_mac,pxe_device,management_device,management_ip_v4,management_ip_v6,application_device,application_ip_v4,application_ip_v6,system_type,application_type,domain,status from servers WHERE global_fk= %s;'
    sql_data = (global_fk,)
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
        server_fk,server,os_version,drive,swapsize,console_port,console_speed,pxe_mac,pxe_device,management_device,management_ip_v4,management_ip_v6,application_device,application_ip_v4,application_ip_v6,system_type,application_type,domain,status = row
        out_buffer = '[server=' + server + ']\nOS_VERSION=' + os_version + '\nDRIVE=' + drive + '\nSWAPSIZE=' + str(swapsize)
        print(out_buffer)
        out_buffer = 'CONSOLE_PORT=' + str(console_port) + '\nCONSOLE_SPEED=' + str(console_speed) + '\nPXE_MAC=' + pxe_mac
        print(out_buffer)
        out_buffer = 'PXE_DEVICE=' + pxe_device + '\nMANAGEMENT_DEVICE=' + management_device + '\nMANAGEMENT_IP_V4=' + management_ip_v4
        print(out_buffer)
        out_buffer = 'MANAGEMENT_IP_V6=' + management_ip_v6 + '\nAPPLICATION_DEVICE=' + application_device
        print(out_buffer)
        out_buffer = 'APPLICATION_IP_V4=' + application_ip_v4 + '\nAPPLICATION_IP_V6=' + application_ip_v6
        print(out_buffer)
        out_buffer = 'SYSTEM_TYPE=' + system_type + '\nAPPLICATION_TYPE=' + application_type + '\nDOMAIN=' + domain
        print(out_buffer)
        out_buffer = 'STATUS=' + status
        print(out_buffer)
        if system_type == 'VBOX':
            print_server_virtual(server_fk,global_fk,server)
        elif 'RACK' in system_type:
            print_server_rack(server_fk,global_fk,server)
        elif 'BLADE' in system_type:
            print_server_blade(server_fk,global_fk,server)
        elif 'OPENSTACK' in system_type:
            print_server_openstack(server_fk,global_fk,server)
        out_buffer = '\n'
        print(out_buffer)

def print_server_virtual(server_fk,global_fk,server):
    sql = 'SELECT vm_type,vm_host,vm_rdp_port,vm_memory,vm_cpu,vm_interface_device,vm_drive_type,vm_iscsi_target,vm_iscsi_port,vm_iscsi_iqn from vm_info WHERE global_fk = %s AND server_fk = %s;'
    sql_data = (global_fk,server_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    row = cur.fetchone()
    cur.close()
    if not len(row):
        out_buffer = 'ERROR reading database table vm_info for server [' + server + ']'
        print(out_buffer)
    vm_type,vm_host,vm_rdp_port,vm_memory,vm_cpu,vm_interface_device,vm_drive_type,vm_iscsi_target,vm_iscsi_port,vm_iscsi_iqn = row
    out_buffer = 'VM_TYPE=' + vm_type + '\nVM_HOST=' + vm_host + '\nVM_RDP_PORT=' + str(vm_rdp_port) + '\nVM_MEMORY=' + str(vm_memory)
    print(out_buffer)
    out_buffer = 'VM_CPU=' + str(vm_cpu) + '\nVM_INTERFACE_DEVICE=' + vm_interface_device + '\nVM_DRIVE_TYPE=' + vm_drive_type
    print(out_buffer)
    out_buffer = 'VM_ISCSI_TARGET=' + vm_iscsi_target + '\nVM_ISCSI_PORT=' + str(vm_iscsi_port) + '\nVM_ISCSI_IQN=' + vm_iscsi_iqn
    print(out_buffer)

def print_server_rack(server_fk,global_fk,server):
    sql = 'SELECT building,floor,row,rack,unit,size,serial_number,ipmi_ip_v4 from rack_info WHERE global_fk = %s AND server_fk = %s;'
    sql_data = (global_fk,server_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    row = cur.fetchone()
    cur.close()
    if not len(row):
        out_buffer = 'ERROR reading database table rack_info for server [' + server + ']'
        print(out_buffer)
    rack_building,rack_floor,rack_row,rack_rack,rack_unit,rack_size,rack_serial,rack_ipmi_ip_v4 = row
    out_buffer = 'RACK_BUILDING=' + rack_building + '\nRACK_FLOOR=' + str(rack_floor) + '\nRACK_ROW=' + str(rack_row)
    print(out_buffer)
    pot_buffer = 'RACK_RACK=' + str(rack_rack) + '\nRACK_UNIT=' + str(rack_unit) + '\nRACK_SERIAL=' + rack_serial 
    print(out_buffer)
    out_buffer = 'RACK_IPMI_IP_V4=' + rack_ipmi_ip_v4
    print(out_buffer)

def print_server_blade(server_fk,kglobal_fk,server):
    sql = 'SELECT blade_center,unit,serial_number,blade_center_ip_v4,ipmi_ip_v4 from blade_info WHERE global_fk = %s AND server_fk = %s;'
    sql_data = (global_fk,server_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    row = cur.fetchone()
    cur.close()
    if not len(row):
        out_buffer = 'ERROR reading database table blade_info for server [' + server + ']'
        print(out_buffer)
    blade_center,blade_unit,blade_serial,blade_ip_v4,blade_ipmi_ip_v4 = row
    out_buffer = 'BLADE_CENTER=' + str(blade_center) + '\nBLADE_UNIT=' + str(blade_unit) + '\nBLADE_SERIAL=' + str( blade_serial)
    print(out_buffer)
    out_buffer = 'BLADE_IP_V4=' + blade_ip_v4 + '\nBLADE_IPMI_IP_V4=' + blade_ipmi_ip_v4
    print(out_buffer)

def print_server_openstack(server_fk,global_fk,server):
    sql = 'SELECT openstack_url,image,flavor,management_network,application_network,ssh_key,security_group,zone from openstack_info WHERE global_fk = %s AND server_fk = %s;'
    sql_data = (global_fk,server_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    row = cur.fetchone()
    cur.close()
    if not len(row):
        out_buffer = 'ERROR reading database table openstack_info for server [' + server + ']'
        print(out_buffer)
    openstack_url,openstack_image,flavor,openstack_management_network,openstack_application_network,openstack_ssh_key,openstack_security_group,openstack_zone = row
    out_buffer = 'OPENSTACK_URL=' + openstack_url + '\nOPENSTACK_IMAGE=' + openstack_image + '\nOPENSTACK_FLAVOR=' + flavor + '\nOPENSTACK_MANAGEMENT_NETWORK=' + openstack_management_network
    print(out_buffer)
    out_buffer = 'OPENSTACK_APPLICATION_NETWORK=' + openstack_application_network + '\nOPENSTACK_SSH_KEY=' + openstack_ssh_key
    print(out_buffer)
    out_buffer = 'OPENSTACK_SECURITY_GROUP=' + openstack_security_group + '\nOPENSTACK_ZONE=' + openstack_zone
    print(out_buffer)


def get_global_fk(dbconn,globalname):
    sql = 'SELECT global_fk FROM globals WHERE global_name = %s;'
    sql_data = (globalname,)
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
# MAIN
#

if __name__ == '__main__':

    configfile = '/home/art/work_stuff/pykick/config/kickstart.config'
    logfile = '/home/art/work_stuff/pykick/logs/kick_config_create.log'
    ks_parms = {}
    dbconn = ''
    globalname = ''
    global_fk = ''
 
    if len(sys.argv) != 2:
        print('Usage: kick_config_create.py3 <CONFIG NAME>')
        raise SystemExit(1)
    globalname = str(sys.argv[1])
    start_logging(logfile)
    get_ks_parms(ks_parms)
    dbconn = open_db(ks_parms)
    global_fk = get_global_fk(dbconn,globalname);
    if not global_fk:
        print('config name ',globalname,' is broken.... Usage: kick_config_create.py3 <CONFIG NAME>')
        close_db(dbconn)
        raise SystemExit(1)
    else:
        out_buffer = '#\n# global section for ' + globalname + '\n#\n'   
        print(out_buffer)
        print_global(dbconn,global_fk,globalname)
        out_buffer = '#\n# subnet section for ' + globalname + '\n#\n'   
        print(out_buffer)
        print_subnet(dbconn,global_fk,globalname)
        out_buffer = '#\n# server section for ' + globalname + '\n#\n'   
        print(out_buffer)
        print_server(dbconn,global_fk,globalname)
        close_db(dbconn)
        print('#kick_config_create completed on config name ',globalname)
        raise SystemExit(1)
