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

def get_ks_parms(configfile,ks_parms):
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
    dblist = ks_parms['DBLIST']
    dbuser = ks_parms['USER']
    dbpass = ks_parms['PASS']
    dbconn = psycopg2.connect(database=dbname,user=dbuser,password=dbpass,host=dbhost,port=dbport)
    logging.info('open_db completed')
    return(dbconn)

def open_list_db(ks_parms):
    dbhost = ks_parms['IP']
    dbport = ks_parms['PORT']
    dbname = ks_parms['DB']
    dblist = ks_parms['DBLIST']
    dbuser = ks_parms['USER']
    dbpass = ks_parms['PASS']
    dbconn_list = psycopg2.connect(database=dblist,user=dbuser,password=dbpass,host=dbhost,port=dbport)
    logging.info('open_list_db completed')
    return(dbconn_list)

def close_db(dbconn):
    dbconn.close()
    logging.info('close_db completed')

def dblist_add(dbconn_list,global_fk,global_name):
    sql = 'INSERT into listkickers (global_fk,global_name) VALUES(%s,%s);'
    sql_data = (global_fk,global_name,)
    cur = dbconn_list.cursor()
    cur.execute(sql,sql_data)
    ret =  cur.statusmessage
    if ret == 'INSERT 0 1':
        dbconn_list.commit()
        logging.info('update_listkicker_db commited INSERT sql=[%s] data=[%s]',sql,sql_data)
    else:
        logging.info('update_listkicker_db commited INSERT FAILED')
    
def read_config_file(dbconn,configfile,global_info,network_info,network_v6_info,server_info):
    global_flag = 0
    network_flag = 0
    network_v6_flag = 0
    server_flag = 0
    network_name = ''
    network_v6_name = ''
    server_name = ''
    
    fh = open(configfile,'rt')
    for line in fh:
       line = line.rstrip('\n')
       line = line.rstrip('\r')

       if (line.startswith('#') or not line) :
           continue
       else:
           if re.search('^\[global=',line):
               global_flag = 1
               network_flag = 0
               network_v6_flag = 0
               server_flag = 0
               line = re.sub('[\[\]]','',line)
               attribute,value =  line.split('=')
               attribute =  attribute.strip(' ')
               value =  value.strip(' ')
               global_info['GLOBAL_NAME'] = value
           elif re.search('^\[subnet_v4=',line):
               global_flag = 0
               network_flag = 1
               network_v6_flag = 0
               server_flag = 0
               network_name = ''
               line = re.sub('[\[\]]','',line)
               attribute,value =  line.split('=')
               attribute =  attribute.strip(' ')
               value =  value.strip(' ')
               network_name = value
               network_info[network_name]['NETWORK_V4_NAME'] = value
           elif re.search('^\[subnet_v6=',line):
               global_flag = 0
               network_flag = 0
               network_v6_flag = 1
               server_flag = 0
               network_v6_name = ''
               line = re.sub('[\[\]]','',line)
               attribute,value =  line.split('=')
               attribute =  attribute.strip(' ')
               value =  value.strip(' ')
               network_v6_name = value
               network_v6_info[network_v6_name]['NETWORK_V6_NAME'] = value
           elif re.search('^\[server=',line):
               global_flag = 0
               network_flag = 0
               network_v6_flag = 0
               server_flag = 1
               server_name = ''
               line = re.sub('[\[\]]','',line)
               attribute,value =  line.split('=')
               attribute =  attribute.strip(' ')
               value =  value.strip(' ')
               server_name = value
               server_info[server_name]['HOSTNAME'] = value
               server_info[server_name]['OS_VERSION'] = 'none'
               server_info[server_name]['CONSOLE_PORT'] = 'none'
               server_info[server_name]['CONSOLE_SPEED'] = 'none' 
               server_info[server_name]['SWAPSIZE'] = 'none' 
               server_info[server_name]['PXE_MAC'] = 'none' 
               server_info[server_name]['PXE_DEVICE'] = 'none'
               server_info[server_name]['MANAGEMENT_DEVICE'] = 'none'
               server_info[server_name]['MANAGEMENT_IP_V4'] = 'none'
               server_info[server_name]['MANAGEMENT_IP_V6'] = 'none'
               server_info[server_name]['APPLICATION_DEVICE'] = 'none'
               server_info[server_name]['APPLICATION_IP_ADDRESS_V4'] = 'none'
               server_info[server_name]['APPLICATION_IP_ADDRESS_V6'] = 'none'
               server_info[server_name]['DOMAIN'] = 'none'
               server_info[server_name]['APPLICATION_TYPE'] = 'none'
               server_info[server_name]['SYSTEM_TYPE'] = 'none'
               server_info[server_name]['STATUS'] = 'PXEBOOT'
           else:
               if global_flag:
                   attribute,value =  line.split('=')
                   attribute =  attribute.strip(' ')
                   value =  value.strip(' ')
                   global_info[attribute] = str(value)
               elif network_flag:
                   attribute,value =  line.split('=')
                   attribute =  attribute.strip(' ')
                   value =  value.strip(' ')
                   network_info[network_name][attribute] = str(value)
               elif network_v6_flag:
                   attribute,value =  line.split('=')
                   attribute =  attribute.strip(' ')
                   value =  value.strip(' ')
                   network_v6_info[network_v6_name][attribute] = str(value)
               elif server_flag:
                   attribute,value =  line.split('=')
                   attribute =  attribute.strip(' ')
                   value =  value.strip(' ')
                   server_info[server_name][attribute] = str(value)

    fh.close()
    logging.info('read_config completed')

def print_config_info(global_info,network_info,network_v6_info,server_info):
    for key in global_info:
        logging.info('global_info[%s] = [%s]',key,global_info[key])

    for key in network_info:
        for subkey in network_info[key]:
            logging.info('network_info[%s][%s]= [%s]',key,subkey,network_info[key][subkey])

    for key in network_v6_info:
        for subkey in network_v6_info[key]:
            logging.info('network_v6_info[%s][%s]= [%s]',key,subkey,network_v6_info[key][subkey])

    for key in server_info:
        for subkey in server_info[key]:
            logging.info('server_info[%s][%s]= [%s]',key,subkey,server_info[key][subkey])

    logging.info('print_config completed')

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

def get_server_fk(dbconn,servername):
    sql = 'SELECT server_fk FROM servers WHERE hostname = %s;'
    sql_data = (servername,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    curret = cur.fetchone()
    if not curret:
        server_fk = 0
    else:
        server_fk = curret[0]
    logging.info('get_server_fk completed %s',server_fk)
    cur.close()
    return(server_fk)

def read_db_config(dbconn,global_fk,global_info,server_info):
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
    global_info['GLOBAL_NAME'],global_info['DHCPD_IP'],global_info['DHCPD_PATH'],global_info['TFTPD_IP'],global_info['TFTPD_PATH'],global_info['HTTP_IP'],global_info['HTTP_TOP'],global_info['OS_PATH'],global_info['SCRIPTS_PATH'],global_info['TEMPLATES_PATH'],global_info['SOFTWARE_PATH'],global_info['VM_PATH'],global_info['OPENSTACK_PATH'],global_info['KEYBOARD'],global_info['TIMEZONE'],global_info['ROOT_PW'],global_info['DEFAULT_USER'],global_info['DEFAULT_USER_PW'],global_info['DNS_SERVERS'],global_info['NTP_SERVERS'],global_info['DOMAIN'],global_info['SEARCH_DOMAINS'],global_info['LOG_SERVER'],global_info['NAGIOS_SERVER'] = rows

    sql = 'SELECT server_fk,hostname,os_version,drive,swap,console_port,console_speed,pxe_mac,pxe_device,management_device,management_ip_v4,management_ip_v6,application_device,application_ip_v4,application_ip_v6,system_type,application_type,domain,status from servers WHERE global_fk= %s AND system_type = %s;'
    sql_data = (global_fk,'OPENSTACK',)
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
        sql = 'SELECT image,flavor,management_network,application_network,ssh_key,security_group,zone from openstack_info WHERE global_fk = %s AND server_fk = %s;'
        sql_data = (global_fk,server_fk,)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        rows = cur.fetchone()
        cur.close()
        if not len(rows):
            out_buffer = 'ERROR reading database table openstack_info for server [' + server + ']'
            print(out_buffer)
        server_info[server]['OPENSTACK_IMAGE'],server_info[server]['OPENSTACK_FLAVOR'],server_info[server]['OPENSTACK_MANAGEMENT_NETWORK'],server_info[server]['OPENSTACK_APPLICATION_NETWORK'],server_info[server]['OPENSTACK_SSH_KEY'],server_info[server]['OPENSTACK_SECURITY_GROUP'],server_info[server]['OPENSTACK_ZONE'] = rows
    return(1)

def update_global_db(dbconn,dbconn_list,global_info):
    global_fk = get_global_fk(dbconn,global_info['GLOBAL_NAME'])
    if global_fk == 0:
        sql = 'INSERT into globals (global_name,dhcpd_ip,dhcpd_path,tftpd_ip,tftpd_path,http_ip,http_top,os_path,scripts_path,templates_path,software_path,vm_path,openstack_path,keyboard,timezone,root_pw,default_user,default_user_pw,dns_servers,ntp_servers,domain,search_domains,log_server,nagios_server) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        sql_data = (global_info['GLOBAL_NAME'],global_info['DHCPD_IP'],global_info['DHCPD_PATH'],global_info['TFTPD_IP'],global_info['TFTPD_PATH'],global_info['HTTP_IP'],global_info['HTTP_TOP'],global_info['OS_PATH'],global_info['SCRIPTS_PATH'],global_info['TEMPLATES_PATH'],global_info['SOFTWARE_PATH'],global_info['VM_PATH'],global_info['OPENSTACK_PATH'],global_info['KEYBOARD'],global_info['TIMEZONE'],global_info['ROOT_PW'],global_info['DEFAULT_USER'],global_info['DEFAULT_USER_PW'],global_info['DNS_SERVERS'],global_info['NTP_SERVERS'],global_info['DOMAIN'],global_info['SEARCH_DOMAINS'],global_info['LOG_SERVER'],global_info['NAGIOS_SERVER'], )
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        ret =  cur.statusmessage
        if ret == 'INSERT 0 1':
            dbconn.commit()
            logging.info('update_global_db commited INSERT sql=[%s] data=[%s]',sql,sql_data)
        else:
            logging.info('update_global_db commited INSERT FAILED')
            exit_error('update_global_db commited INSERT FAILED')
        cur.close()
        global_fk = get_global_fk(dbconn,global_info['GLOBAL_NAME'])
        dblist_add(dbconn_list,global_fk,global_info['GLOBAL_NAME'])
    else:
        sql = 'UPDATE globals set dhcpd_ip = %s, dhcpd_path = %s, tftpd_ip = %s, tftpd_path = %s, http_ip = %s, http_top = %s, os_path = %s, scripts_path = %s, templates_path = %s ,software_path = %s, vm_path = %s, openstack_path = %s, keyboard = %s, timezone = %s, root_pw = %s, default_user = %s, default_user_pw = %s, dns_servers = %s, ntp_servers = %s, domain = %s, search_domains = %s, log_server = %s, nagios_server = %s WHERE global_name = %s AND global_fk = %s;'
        sql_data = (global_info['DHCPD_IP'],global_info['DHCPD_PATH'],global_info['TFTPD_IP'],global_info['TFTPD_PATH'],global_info['HTTP_IP'],global_info['HTTP_TOP'],global_info['OS_PATH'],global_info['SCRIPTS_PATH'],global_info['TEMPLATES_PATH'],global_info['SOFTWARE_PATH'],global_info['VM_PATH'],global_info['OPENSTACK_PATH'],global_info['KEYBOARD'],global_info['TIMEZONE'],global_info['ROOT_PW'],global_info['DEFAULT_USER'],global_info['DEFAULT_USER_PW'],global_info['DNS_SERVERS'],global_info['NTP_SERVERS'],global_info['DOMAIN'],global_info['SEARCH_DOMAINS'],global_info['LOG_SERVER'],global_info['NAGIOS_SERVER'],global_info['GLOBAL_NAME'],global_fk, )
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        ret =  cur.statusmessage
        if ret == 'UPDATE 1':
            dbconn.commit()
            logging.info('update_global_db commited UPDATE sql=[%s] data=[%s]',sql,sql_data)
        else:
            logging.info('update_global_db commited INSERT FAILED')
        cur.close()
    logging.info('update_global_db completed')


def update_network_db(dbconn,global_info,network_info):
    global_fk = get_global_fk(dbconn,global_info['GLOBAL_NAME'])
    if global_fk == 0:
        logging.info('update_network_db failed as global_fk is 0')
        close_db(dbconn)
        exit_error('update_network_db failed as global_fk is 0')
    for key in network_info:
        sql = 'select subnet_v4_fk from subnet_v4 WHERE subnet_name = %s'
        sql_data = (network_info[key]['NETWORK_V4_NAME'],)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        curret = cur.fetchone()
        if not curret:
            subnet_v4_fk = 0
        else:
            subnet_v4_fk = curret[0]
        cur.close()
        if not subnet_v4_fk:
            sql = 'INSERT into subnet_v4 (global_fk,subnet_name,subnet_description,subnet_network,subnet_netmask,subnet_router,subnet_dhcp) VALUES (%s,%s,%s,%s,%s,%s,%s);'
            sql_data = (global_fk,network_info[key]['NETWORK_V4_NAME'],network_info[key]['DESCRIPTION'],network_info[key]['NETWORK'],network_info[key]['NETMASK'],network_info[key]['ROUTER'],network_info[key]['DHCP'],)
            cur = dbconn.cursor()
            cur.execute(sql,sql_data)
            ret =  cur.statusmessage
            if ret == 'INSERT 0 1':
                dbconn.commit()
                logging.info('update_network_db commited INSERT sql=[%s] data=[%s]',sql,sql_data)
            else:
                logging.info('update_network_db commited INSERT FAILED')
            cur.close()
        else:
            sql = 'UPDATE subnet_v4 set subnet_name = %s, subnet_description = %s, subnet_network = %s, subnet_netmask = %s, subnet_router = %s, subnet_dhcp = %s  WHERE subnet_v4_fk = %s AND global_fk = %s;'
            sql_data = (network_info[key]['NETWORK_V4_NAME'],network_info[key]['DESCRIPTION'],network_info[key]['NETWORK'],network_info[key]['NETMASK'],network_info[key]['ROUTER'],network_info[key]['DHCP'],subnet_v4_fk,global_fk,)
            cur = dbconn.cursor()
            cur.execute(sql,sql_data)
            ret =  cur.statusmessage
            if ret == 'UPDATE 1':
                dbconn.commit()
                logging.info('update_network_db commited UPDATE sql=[%s] data=[%s]',sql,sql_data)
            else:
                logging.info('update_network_db commited INSERT FAILED')
            cur.close()
    logging.info('update_network_db completed')


def update_network_v6_db(dbconn,global_info,network_v6_info):
    global_fk = get_global_fk(dbconn,global_info['GLOBAL_NAME'])
    if global_fk == 0:
        logging.info('update_network_v6_db failed as global_fk is 0')
        close_db(dbconn)
        exit_error('update_network_v6_db failed as global_fk is 0')
    for key in network_v6_info:
        sql = 'select subnet_v6_fk from subnet_v6 WHERE subnet_name = %s'
        sql_data = (network_v6_info[key]['NETWORK_V6_NAME'],)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        curret = cur.fetchone()
        if not curret:
            subnet_v6_fk = 0
        else:
            subnet_v6_fk = curret[0]
        cur.close()
        if not subnet_v6_fk:
            sql = 'INSERT into subnet_v6 (global_fk,subnet_name,subnet_description,subnet_network,subnet_netmask,subnet_router,subnet_dhcp) VALUES (%s,%s,%s,%s,%s,%s,%s);'
            sql_data = (global_fk,network_v6_info[key]['NETWORK_V6_NAME'],network_v6_info[key]['DESCRIPTION'],network_v6_info[key]['NETWORK'],network_v6_info[key]['NETMASK'],network_v6_info[key]['ROUTER'],network_v6_info[key]['DHCP'],)
            cur = dbconn.cursor()
            cur.execute(sql,sql_data)
            ret =  cur.statusmessage
            if ret == 'INSERT 0 1':
                dbconn.commit()
                logging.info('update_network_v6_db commited INSERT sql=[%s] data=[%s]',sql,sql_data)
            else:
                logging.info('update_network_v6_db commited INSERT FAILED')
            cur.close()
        else:
            sql = 'UPDATE subnet_v6 set subnet_name = %s, subnet_description = %s, subnet_network = %s, subnet_netmask = %s, subnet_router = %s, subnet_dhcp = %s WHERE subnet_v6_fk = %s AND global_fk = %s;'
            sql_data = (network_v6_info[key]['NETWORK_V6_NAME'],network_v6_info[key]['DESCRIPTION'],network_v6_info[key]['NETWORK'],network_v6_info[key]['NETMASK'],network_v6_info[key]['ROUTER'],network_v6_info[key]['DHCP'],subnet_v6_fk,global_fk,)
            cur = dbconn.cursor()
            cur.execute(sql,sql_data)
            ret =  cur.statusmessage
            if ret == 'UPDATE 1':
                dbconn.commit()
                logging.info('update_network_v6_db commited UPDATE sql=[%s] data=[%s]',sql,sql_data)
            else:
                logging.info('update_network_v6_db commited INSERT FAILED')
            cur.close()
    logging.info('update_network_v6_db completed')

def update_server_db(dbconn,global_info,server_info):
    global_fk = get_global_fk(dbconn,global_info['GLOBAL_NAME'])
    if global_fk == 0:
        logging.info('update_server_db failed as global_fk is 0')
        close_db(dbconn)
        exit_error('update_server_db failed as global_fk is 0')
    for key in server_info:
        sql = 'select server_fk from servers WHERE hostname = %s'
        sql_data = (server_info[key]['HOSTNAME'],)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        curret = cur.fetchone()
        if not curret:
            server_fk = 0
        else:
            server_fk = curret[0]
        cur.close()
        if not server_fk:
            sql = 'INSERT into servers (global_fk,hostname,os_version,drive,swap,console_port,console_speed,pxe_mac,pxe_device,management_device,management_ip_v4,management_ip_v6,application_device,application_ip_v4,application_ip_v6,system_type,application_type,domain,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            sql_data = (global_fk,server_info[key]['HOSTNAME'],server_info[key]['OS_VERSION'],server_info[key]['DRIVE'],server_info[key]['SWAPSIZE'],server_info[key]['CONSOLE_PORT'],server_info[key]['CONSOLE_SPEED'],server_info[key]['PXE_MAC'],server_info[key]['PXE_DEVICE'],server_info[key]['MANAGEMENT_DEVICE'],server_info[key]['MANAGEMENT_IP_V4'],server_info[key]['MANAGEMENT_IP_V6'],server_info[key]['APPLICATION_DEVICE'],server_info[key]['APPLICATION_IP_V4'],server_info[key]['APPLICATION_IP_V6'],server_info[key]['SYSTEM_TYPE'],server_info[key]['APPLICATION_TYPE'],server_info[key]['DOMAIN'],server_info[key]['STATUS'],)
            cur = dbconn.cursor()
            cur.execute(sql,sql_data)
            ret =  cur.statusmessage
            if ret == 'INSERT 0 1':
                dbconn.commit()
                logging.info('update_server_db commited INSERT sql=[%s] data=[%s]',sql,sql_data)
            else:
                logging.info('update_server_db commited INSERT FAILED')
            cur.close()
        else:
            sql = 'UPDATE servers set hostname=%s,os_version=%s,drive=%s,swap=%s,console_port=%s,console_speed=%s,pxe_mac=%s,pxe_device=%s,management_device=%s,management_ip_v4=%s,management_ip_v6=%s,application_device=%s,application_ip_v4=%s,application_ip_v6=%s,system_type=%s,application_type=%s,domain=%s,status=%s WHERE server_fk=%s AND global_fk=%s;'
            sql_data = (server_info[key]['HOSTNAME'],server_info[key]['OS_VERSION'],server_info[key]['DRIVE'],server_info[key]['SWAPSIZE'],server_info[key]['CONSOLE_PORT'],server_info[key]['CONSOLE_SPEED'],server_info[key]['PXE_MAC'],server_info[key]['PXE_DEVICE'],server_info[key]['MANAGEMENT_DEVICE'],server_info[key]['MANAGEMENT_IP_V4'],server_info[key]['MANAGEMENT_IP_V6'],server_info[key]['APPLICATION_DEVICE'],server_info[key]['APPLICATION_IP_V4'],server_info[key]['APPLICATION_IP_V6'],server_info[key]['SYSTEM_TYPE'],server_info[key]['APPLICATION_TYPE'],server_info[key]['DOMAIN'],server_info[key]['STATUS'],server_fk,global_fk,)
            cur = dbconn.cursor()
            cur.execute(sql,sql_data)
            ret =  cur.statusmessage
            if ret == 'UPDATE 1':
                dbconn.commit()
                logging.info('update_server_db commited UPDATE sql=[%s] data=[%s]',sql,sql_data)
            else:
                logging.info('update_server_db commited INSERT FAILED')
            cur.close()
        if server_info[key]['SYSTEM_TYPE'] == 'VBOX':
            update_vserver_db(dbconn,global_fk,key,server_info)
        elif 'RACK' in server_info[key]['SYSTEM_TYPE']:
            update_rack_db(dbconn,global_fk,key,server_info)
        elif 'BLADE' in server_info[key]['SYSTEM_TYPE']:
            update_blade_db(dbconn,global_fk,key,server_info)
        elif 'OPENSTACK' in server_info[key]['SYSTEM_TYPE']:
            update_openstack_db(dbconn,global_fk,key,server_info)
    logging.info('update_server_db completed')

def update_vserver_db(dbconn,global_fk,server,server_info):
    server_fk = get_server_fk(dbconn,server)
    if server_fk == 0:
        logging.info('update_vserver_db failed as server_fk is 0')
        close_db(dbconn)
        exit_error('update_vserver_db failed as server_fk is 0')
    sql = 'select vm_fk from vm_info WHERE global_fk = %s AND server_fk = %s'
    sql_data = (global_fk,server_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    curret = cur.fetchone()
    if not curret:
        vm_fk = 0
    else:
        vm_fk = curret[0]
    cur.close()
    if not vm_fk:
        sql = 'INSERT into vm_info (global_fk,server_fk,vm_type,vm_host,vm_rdp_port,vm_memory,vm_cpu,vm_interface_device,vm_drive_type,vm_iscsi_target,vm_iscsi_port,vm_iscsi_iqn) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        sql_data = (global_fk,server_fk,server_info[server]['VM_TYPE'],server_info[server]['VM_HOST'],server_info[server]['VM_RDP_PORT'],server_info[server]['VM_MEMORY'],server_info[server]['VM_CPU'],server_info[server]['VM_INTERFACE_DEVICE'],server_info[server]['VM_DRIVE_TYPE'],server_info[server]['VM_ISCSI_TARGET'],server_info[server]['VM_ISCSI_PORT'],server_info[server]['VM_ISCSI_IQN'])
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        ret =  cur.statusmessage
        if ret == 'INSERT 0 1':
            dbconn.commit()
            logging.info('update_vserver_db commited INSERT sql=[%s] data=[%s]',sql,sql_data)
        else:
            logging.info('update_vserver_db commited INSERT FAILED')
        cur.close()
    else:
        sql = 'UPDATE vm_info set vm_type=%s,vm_host=%s,vm_rdp_port=%s,vm_memory=%s,vm_cpu=%s,vm_interface_device=%s,vm_drive_type=%s,vm_iscsi_target=%s,vm_iscsi_port=%s,vm_iscsi_iqn=%s WHERE vm_fk=%s AND global_fk=%s AND server_fk = %s;'
        sql_data = (server_info[server]['VM_TYPE'],server_info[server]['VM_HOST'],server_info[server]['VM_RDP_PORT'],server_info[server]['VM_MEMORY'],server_info[server]['VM_CPU'],server_info[server]['VM_INTERFACE_DEVICE'],server_info[server]['VM_DRIVE_TYPE'],server_info[server]['VM_ISCSI_TARGET'],server_info[server]['VM_ISCSI_PORT'],server_info[server]['VM_ISCSI_IQN'],vm_fk,global_fk,server_fk)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        ret =  cur.statusmessage
        if ret == 'UPDATE 1':
            dbconn.commit()
            logging.info('update_vserver_db commited UPDATE sql=[%s] data=[%s]',sql,sql_data)
        else:
            logging.info('update_vserver_db commited INSERT FAILED')
        cur.close()
    logging.info('update_vserver_db completed')

def update_rack_db(dbconn,global_fk,server,server_info):
    server_fk = get_server_fk(dbconn,server)
    if server_fk == 0:
        logging.info('update_rack_db failed as server_fk is 0')
        close_db(dbconn)
        exit_error('update_rack_db failed as server_fk is 0')
    sql = 'select rack_fk from rack_info WHERE global_fk = %s AND server_fk = %s'
    sql_data = (global_fk,server_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    curret = cur.fetchone()
    if not curret:
        rack_fk = 0
    else:
        rack_fk = curret[0]
    cur.close()
    if not rack_fk:
        sql = 'INSERT into rack_info (global_fk,server_fk,building,floor,row,rack,unit,size,serial_number,ipmi_ip_v4) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        sql_data = (global_fk,server_fk,server_info[server]['RACK_BUILDING'],server_info[server]['RACK_FLOOR'],server_info[server]['RACK_ROW'],server_info[server]['RACK_RACK'],server_info[server]['RACK_UNIT'],server_info[server]['RACK_SIZE'],server_info[server]['RACK_SERIAL'],server_info[server]['RACK_IPMI_IP_V4'],)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        ret =  cur.statusmessage
        if ret == 'INSERT 0 1':
            dbconn.commit()
            logging.info('update_rack_db commited INSERT sql=[%s] data=[%s]',sql,sql_data)
        else:
            logging.info('update_rack_db commited INSERT FAILED')
        cur.close()
    else:
        sql = 'UPDATE rack_info set building=%s,floor=%s,row=%s,rack=%s,unit=%s,size=%s,serial_number=%s,ipmi_ip_v4=%s WHERE rack_fk=%s AND global_fk=%s AND server_fk=%s;'
        sql_data = (server_info[server]['RACK_BUILDING'],server_info[server]['RACK_FLOOR'],server_info[server]['RACK_ROW'],server_info[server]['RACK_RACK'],server_info[server]['RACK_UNIT'],server_info[server]['RACK_SIZE'],server_info[server]['RACK_SERIAL'],server_info[server]['RACK_IPMI_IP_V4'],rack_fk,global_fk,server_fk,)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        ret =  cur.statusmessage
        if ret == 'UPDATE 1':
            dbconn.commit()
            logging.info('update_rack_db commited UPDATE sql=[%s] data=[%s]',sql,sql_data)
        else:
            logging.info('update_rack_db commited INSERT FAILED')
        cur.close()
    logging.info('update_rack_db completed')

def update_blade_db(dbconn,global_fk,server,server_info):
    server_fk = get_server_fk(dbconn,server)
    if server_fk == 0:
        logging.info('update_blade_db failed as server_fk is 0')
        close_db(dbconn)
        exit_error('update_rack_db failed as server_fk is 0')
    sql = 'select blade_fk from blade_info WHERE global_fk = %s AND server_fk = %s'
    sql_data = (global_fk,server_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    curret = cur.fetchone()
    if not curret:
        blade_fk = 0
    else:
        blade_fk = curret[0]
    cur.close()
    if blade_fk == 0:
        sql = 'INSERT into blade_info (global_fk,server_fk,blade_center,unit,serial_number,blade_center_ip_v4,ipmi_ip_v4) VALUES(%s,%s,%s,%s,%s,%s,%s);'
        sql_data = (global_fk,server_fk,server_info[server]['BLADE_CENTER'],server_info[server]['BLADE_UNIT'],server_info[server]['BLADE_SERIAL'],server_info[server]['BLADE_IP_V4'],server_info[server]['BLADE_IPMI_IP_V4'],)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        ret =  cur.statusmessage
        if ret == 'INSERT 0 1':
            dbconn.commit()
            logging.info('update_blade_db commited INSERT sql=[%s] data=[%s]',sql,sql_data)
        else:
            logging.info('update_blade_db commited INSERT FAILED')
        cur.close()
    else:
        sql = 'UPDATE blade_info set blade_center=%s,unit=%s,serial_number=%s,blade_center_ip_v4=%s,ipmi_ip_v4=%s WHERE blade_fk = %s AND global_fk = %s AND server_fk = %s;'
        sql_data = (server_info[server]['BLADE_CENTER'],server_info[server]['BLADE_UNIT'],server_info[server]['BLADE_SERIAL'],server_info[server]['BLADE_IP_V4'],server_info[server]['BLADE_IPMI_IP_V4'],blade_fk,global_fk,server_fk,)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        ret =  cur.statusmessage
        if ret == 'UPDATE 1':
            dbconn.commit()
            logging.info('update_blade_db commited UPDATE sql=[%s] data=[%s]',sql,sql_data)
        else:
            logging.info('update_blade_db commited INSERT FAILED')
        cur.close()
    logging.info('update_vserver_db completed')

def update_openstack_db(dbconn,global_fk,server,server_info):
    server_fk = get_server_fk(dbconn,server)
    if server_fk == 0:
        logging.info('update_openstack_db failed as server_fk is 0')
        close_db(dbconn)
        exit_error('update_openstack_db failed as server_fk is 0')
    sql = 'select openstack_fk from openstack_info WHERE global_fk = %s AND server_fk = %s'
    sql_data = (global_fk,server_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    curret = cur.fetchone()
    if not curret:
        openstack_fk = 0
    else:
        openstack_fk = curret[0]
    cur.close()
    if not openstack_fk:
        sql = 'INSERT into openstack_info (global_fk,server_fk,openstack_url,image,flavor,management_network,application_network,ssh_key,security_group,zone) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        sql_data = (global_fk,server_fk,server_info[server]['OPENSTACK_URL'],server_info[server]['OPENSTACK_IMAGE'],server_info[server]['OPENSTACK_FLAVOR'],server_info[server]['OPENSTACK_MANAGEMENT_NETWORK'],server_info[server]['OPENSTACK_APPLICATION_NETWORK'],server_info[server]['OPENSTACK_SSH_KEY'],server_info[server]['OPENSTACK_SECURITY_GROUP'],server_info[server]['OPENSTACK_ZONE'])
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        ret =  cur.statusmessage
        if ret == 'INSERT 0 1':
            dbconn.commit()
            logging.info('update_oenstack_db commited INSERT sql=[%s] data=[%s]',sql,sql_data)
        else:
            logging.info('update_openstack_db commited INSERT FAILED')
        cur.close()
    else:
        sql = 'UPDATE openstack_info set openstack_url=%s,image=%s,flavor=%s,management_network=%s,application_network=%s,ssh_key=%s,security_group=%s,zone=%s WHERE openstack_fk=%s AND global_fk=%s AND server_fk=%s;'
        sql_data = (server_info[server]['OPENSTACK_URL'],server_info[server]['OPENSTACK_IMAGE'],server_info[server]['OPENSTACK_FLAVOR'],server_info[server]['OPENSTACK_MANAGEMENT_NETWORK'],server_info[server]['OPENSTACK_APPLICATION_NETWORK'],server_info[server]['OPENSTACK_SSH_KEY'],server_info[server]['OPENSTACK_SECURITY_GROUP'],server_info[server]['OPENSTACK_ZONE'],openstack_fk,global_fk,server_fk)
        cur = dbconn.cursor()
        cur.execute(sql,sql_data)
        ret =  cur.statusmessage
        if ret == 'UPDATE 1':
            dbconn.commit()
            logging.info('update_openstack_db commited UPDATE sql=[%s] data=[%s]',sql,sql_data)
        else:
            logging.info('update_openstack_db commited INSERT FAILED')
        cur.close()
    logging.info('update_openstack_db completed')

def get_broadcast(subnet_address,netmask):
    import ipaddress

    innet = str(subnet_address) + '/' + str(netmask)
    net = ipaddress.IPv4Network(innet)

    if net:
       bcast = str(net.broadcast_address)
    else:
       bcast = '0'

    logging.info('get_broadcast network [%s]/[%s] completed return [%s]',subnet_address,netmask,bcast)
    return(bcast)


def get_network(ip,netmask):
    import ipaddress

    innet = str(ip) + '/' + str(netmask)
    net = ipaddress.IPv4Interface(innet)

    if net:
        network = re.sub('/\d\d','',str(net.network))
    else:
        network = '0'
    logging.info('get_network [%s]/[%s] completed return [%s]',ip,netmask,network)
    return(network)


def get_network_v6(ip_v6,netmask_v6):
    import ipaddress

    innet = str(ip_v6) + '/' + str(netmask_v6)
    innet = innet.lower()
    net = ipaddress.IPv6Interface(innet)

    if net:
        network_v6 = re.sub('/\d\d','',str(net.network))
        network_v6 = network_v6.lower()
    else:
        network_v6 = '0'
    logging.info('get_network_v6 [%s]/[%s] completed return [%s]',ip_v6,netmask_v6,network_v6)
    return(network_v6)

def get_subnet_network(ip,network_info):
    import ipaddress

    for key in network_info:
        subnet_ip = network_info[key]['NETWORK']
        netmask = network_info[key]['NETMASK']
        network = get_network(ip,netmask)

        if network == subnet_ip:
            logging.info('get_subnet_network [%s] completed return [%s]',ip,subnet_ip)
            return(subnet_ip)
    subnet_ip = '0'
    logging.info('get_subnet_network [%s] completed return [%s]',ip,subnet_ip)
    return(subnet_ip)


def get_subnet_network_v6(ip_v6,network_v6_info):
    import ipaddress

    for key in network_v6_info:
        subnet_ip_v6 = network_v6_info[key]['NETWORK']
        subnet_ip_v6 = subnet_ip_v6.lower()
        netmask_v6 = network_v6_info[key]['NETMASK']
        netmask_v6 = netmask_v6.lower()
        network_v6 = get_network_v6(ip_v6,netmask_v6)
        network_v6 = network_v6.lower()
        if network_v6 == subnet_ip_v6:
            logging.info('get_subnet_network_v6 [%s] completed return [%s]',ip_v6,subnet_ip_v6)
            return(subnet_ip_v6)

    subnet_ip_v6 = '0'
    logging.info('get_subnet_network_v6 [%s] completed return [%s]',ip_v6,subnet_ip_v6)
    return(subnet_ip_v6)


def get_router(network,network_info):

    for key in network_info:
        subnet_ip = network_info[key]['NETWORK']
        router = network_info[key]['ROUTER']

        if subnet_ip == network:
            logging.info('get_router [%s] completed return [%s]',network,router)
            return(router)
    router = '0' 
    logging.info('get_router [%s] completed return [%s]',network,router)
    return(router)


def get_router_v6(network_v6,network_v6_info):

    for key in network_v6_info:
        subnet_ip_v6 = network_v6_info[key]['NETWORK']
        subnet_ip_v6 = subnet_ip_v6.lower()
        router_v6 = str(network_v6_info[key]['ROUTER'])
        router_v6 = router_v6.lower()

        if subnet_ip_v6 == network_v6:
            logging.info('get_router_v6 [%s] completed return [%s]',network_v6,router_v6)
            return(router_v6)
    router_v6 = '0'
    logging.info('get_router_v6 [%s] completed return [%s]',network_v6,router_v6)
    return(router_v6)


def get_netmask(network,network_info):
    for key in network_info:
        subnet_ip = network_info[key]['NETWORK']
        netmask = network_info[key]['NETMASK']

        if subnet_ip == network:
            logging.info('get_netmask [%s] completed return [%s]',network,netmask)
            return(netmask)
    netmask = '0'
    logging.info('get_netmask [%s] completed return [%s]',network,netmask)
    return(netmask)


def get_netmask_v6(network_v6,network_v6_info):
    for key in network_v6_info:
        subnet_ip_v6 = network_v6_info[key]['NETWORK']
        subnet_ip_v6 = subnet_ip_v6.lower()
        netmask_v6 = str(network_v6_info[key]['NETMASK'])
        netmask_v6 = netmask_v6.lower()

        if subnet_ip_v6 == network_v6:
            logging.info('get_netmask_v6 [%s] completed return [%s]',network_v6,netmask_v6)
            return(netmask_v6)

    netmask_v6 = '0'
    logging.info('get_netmask_v6 [%s] completed return [%s]',network_v6,netmask_v6)
    return(netmask_v6)



def check_server_network(global_info,server_info,network_info,network_v6_info):
    server_name = ''
    server_list = []

    for key in server_info:
        for subkey in server_info[key]:
            if subkey == 'HOSTNAME':
                server_name = server_info[key][subkey]
                server_list.append(server_name)

    for server in server_list:
        logging.info('check_server_network server=[%s]',server)
        if server_info[server]['APPLICATION_IP_V4'] == 'none':
            server_info[server]['APPLICATION_GATEWAY_V4'] = 'none'
            server_info[server]['APPLICATION_NETMASK_V4'] = 'none'
            server_info[server]['APPLICATION_NETWORK_V4'] = 'none'
            server_info[server]['APPLICATION_BROADCAST_V4'] = 'none'
        else:
            ip = server_info[server]['APPLICATION_IP_V4']
            subnet_network = get_subnet_network(ip,network_info)
            if subnet_network == '0':
                out_buffer = 'APPLICATION_IP_V4[' + ip + '] for server[' + server + '] is not in SUBNET SECTION....fix the cfg and db....'
                print(out_buffer)
                exit_error(out_buffer)
            netmask = get_netmask(subnet_network,network_info)
            gateway = get_router(subnet_network,network_info)
            broadcast = get_broadcast(subnet_network,netmask)
            server_info[server]['APPLICATION_NETWORK_V4'] = subnet_network
            server_info[server]['APPLICATION_NETMASK_V4'] = netmask
            server_info[server]['APPLICATION_GATEWAY_V4']  = gateway
            server_info[server]['APPLICATION_BROADCAST_V4'] = broadcast
        if server_info[server]['APPLICATION_IP_V6'] == 'none':
            server_info[server]['APPLICATION_NETWORK_V6'] = 'none'
            server_info[server]['APPLICATION_NETMASK_V6'] = 'none'
            server_info[server]['APPLICATION_GATEWAY_V6'] = 'none'
        else:
            ip_v6 = server_info[server]['APPLICATION_IP_V6']
            subnet_network_v6 = get_subnet_network_v6(ip_v6,network_v6_info)
            if subnet_network_v6 == '0':
                out_buffer = 'APPLICATION_IP_V6[' + ip_v6 + '] for server[' + server + '] is not in SUBNET SECTION....fix the cfg and db....'
                print(out_buffer)
                exit_error(out_buffer)
            subnet_netmask_v6 = get_netmask_v6(subnet_network_v6,network_v6_info)
            gateway_v6 = get_router_v6(subnet_network_v6,network_v6_info)
            server_info[server]['APPLICATION_NETWORK_V6'] = subnet_network_v6
            server_info[server]['APPLICATION_NETMASK_V6'] = subnet_netmask_v6
            server_info[server]['APPLICATION_GATEWAY_V6'] = gateway_v6

        if server_info[server]['MANAGEMENT_IP_V4'] == 'none':
            server_info[server]['MANAGEMENT_NETMASK_V4'] = 'none'
            server_info[server]['MANAGEMENT_NETWORK_V4'] = 'none'
            server_info[server]['MANAGEMENT_GATEWAY_V4'] = 'none'
            server_info[server]['MANAGEMENT_BROADCAST_V4'] = 'none'
        else:
            ip = server_info[server]['MANAGEMENT_IP_V4']
            subnet_network = get_subnet_network(ip,network_info)
            if subnet_network == '0':
                out_buffer = 'MANAGEMENT_IP_V4[' + ip + '] for server[' + server + '] is not in SUBNET SECTION....fix the cfg and db....'
                print(out_buffer)
                exit_error(out_buffer)
            netmask = get_netmask(subnet_network,network_info)
            gateway = get_router(subnet_network,network_info)
            broadcast = get_broadcast(subnet_network,netmask)
            server_info[server]['MANAGEMENT_IP_V4'] = subnet_network
            server_info[server]['MANAGEMENT_GATEWAY_V4'] = gateway
            server_info[server]['MANAGEMENT_NETMASK_V4'] = netmask
            server_info[server]['MANAGEMENT_BROADCAST_V4'] = broadcast
        if server_info[server]['MANAGEMENT_IP_V6'] == 'none':
            server_info[server]['MANAGEMENT_NETMASK_V6'] = 'none'
            server_info[server]['MANAGEMENT_NETWORK_V6'] = 'none'
            server_info[server]['MANAGEMENT_GATEWAY_V6'] = 'none'
        else:
            ip_v6 = server_info[server]['MANAGEMENT__IP_V6']
            subnet_network_v6 = get_subnet_network_v6(ip_v6,network_v6_info)
            if subnet_network_v6 == '0':
                out_buffer = 'MANAGEMENT_IP_V6[' + ip_v6 + '] for server[' + server + '] is not in SUBNET SECTION....fix the cfg and db....'
                print(out_buffer)
                exit_error(out_buffer)
            subnet_netmask_v6 = get_netmask_v6(subnet_network_v6,network_v6_info)
            gateway_v6 = get_router_v6(subnet_network_v6,network_v6_info)
            server_info[server]['MANAGEMENT_NETWORK_V6'] = subnet_network_v6
            server_info[server]['MANAGEMENT_NETMASK_V6'] = subnet_netmask_v6
            server_info[server]['MANAGEMENT_GATEWAY_V6'] = gateway_v6
    logging.info('check_server_network completed')

def read_db_network_config(dbconn,global_fk,network_info,network_v6_info):
    sql = 'SELECT subnet_name,subnet_description,subnet_network,subnet_netmask,subnet_router,subnet_dhcp from subnet_v4 WHERE global_fk= %s;'
    sql_data = (global_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    rows = cur.fetchall()
    cur.close()
    if not len(rows):
        out_buffer = 'ERROR reading database table subnet_v4 for gobal_fk [' + global_fk + ']'
        print(out_buffer)
        return(0)
    for row in rows:
        key = row[0]
        network_info[key]['NETWORK_V4_NAME'],network_info[key]['DESCRIPTION'],network_info[key]['NETWORK'],network_info[key]['NETMASK'],network_info[key]['ROUTER'],network_info[key]['DHCP']  = row

    sql = 'SELECT subnet_name,subnet_description,subnet_network,subnet_netmask,subnet_router,subnet_dhcp from subnet_v6 WHERE global_fk= %s;'
    sql_data = (global_fk,)
    cur = dbconn.cursor()
    cur.execute(sql,sql_data)
    rows = cur.fetchall()
    cur.close()
    if not len(rows):
        out_buffer = 'ERROR reading database table subnet_v6 for gobal_fk [' + global_fk + ']'
        print(out_buffer)
        return(0)
    for row in rows:
        key = row[0]
        network_v6_info[key]['NETWORK_V6_NAME'],network_v6_info[key]['DESCRIPTION'],network_v6_info[key]['NETWORK'],network_v6_info[key]['NETMASK'],network_v6_info[key]['ROUTER'],network_v6_info[key]['DHCP'] = row
    return(1)

def setup_dhcp(global_info,network_info,ks_parms):
    domains = global_info['SEARCH_DOMAINS']
    domains = re.sub('[,]',' ',domains)
    dns_servers = global_info['DNS_SERVERS']    
    location = ks_parms['LOCATION']

    dhcpd_file = global_info['DHCPD_PATH'] + '/dhcpd.conf'
    dhcpd_subnet_file = global_info['DHCPD_PATH'] + '/dhcpd-kickstart-subnet.conf'
    dhcpd_hosts_file = global_info['DHCPD_PATH'] + '/dhcpd-kickstart-hosts.conf'
    fh = open(dhcpd_file,'w')
    fh.write('ddns-update-style none;\n')
    fh.write('log-facility daemon;\n')
    fh.write('authoritative;\n')
    fh.write('include "' + dhcpd_subnet_file + '"\n')
    fh.write('include "' + dhcpd_hosts_file + '"\n')
    fh.close()
    fh = open(dhcpd_subnet_file,'w')

    for key in network_info:
        subnet_ip = network_info[key]['NETWORK']
        netmask = network_info[key]['NETMASK']
        router = network_info[key]['ROUTER']
        dhcp_flag = int(network_info[key]['DHCP'])

        if dhcp_flag == 1:
            broadcast_address = str(get_broadcast(subnet_ip,netmask))
            fh.write('# SUBNET ' + subnet_ip + '\n#\n')
            fh.write('subnet ' + subnet_ip + ' netmask ' + netmask + ' {\n')
            fh.write('  option domain-name-servers ' + dns_servers + ';\n')
            fh.write('  option broadcast-address ' + broadcast_address + ';\n')
            fh.write('  option routers '+ router + ';\n')
            fh.write('  option domain-name "' + domains + '";\n}\n\n#\n')

    fh.close()
    fh = open(dhcpd_hosts_file,'w')
    fh.write('#\n# HOSTS DHCPD INCLUDE FILE\n#\n')
    fh.close()
    logging.info('setup_dhcpd completed')

def setup_tftpd(global_info,ks_parms):
    import glob
    location = ks_parms['LOCATION']
    tftpd_dir = global_info['TFTPD_PATH']
    tftpd_dir = tftpd_dir + '/pxelinux.cfg/'
    os.chdir(tftpd_dir)
    tftpd_files =  glob.glob('01-*')
    for filename in tftpd_files:
        logging.info('setup_tftpd unlink %s/%s',tftpd_dir,filename)
        os.unlink(filename)
    logging.info('setup_tftpd completed')

def setup_servers(global_info,network_info,server_info,ks_parms):
    import glob
    from shutil import copyfile
    import fileinput

    tftpd_path = global_info['TFTPD_PATH'] + '/pxelinux.cfg'
    nameservers = global_info['DNS_SERVERS']    
    dns_nameserver,dns_nameserver2,dns_nameserver3 = nameservers.split(',')
    http_server_ip = global_info['HTTP_IP']
    ks_http_location = 'http://' + http_server_ip + '/' + global_info['HTTP_TOP'] + '/scripts'
    os_path = global_info['OS_PATH']
    scripts_path = global_info['SCRIPTS_PATH']
    templates_path = global_info['TEMPLATES_PATH']
    software_path = global_info['SOFTWARE_PATH']
    vm_path = global_info['VM_PATH']
    os.chdir(scripts_path)
    script_files = glob.glob('*') 

    for filename in script_files:
        if os.path.isfile(filename):
            logging.info('setup_servers unlink %s/%s',scripts_path,filename)
            os.unlink(filename)

    server_list = []
    for key in server_info:
        for subkey in server_info[key]:
            if subkey == 'HOSTNAME':
                server = server_info[key][subkey]
                server_list.append(server)

    for server in server_list:
        logging.info('setup_servers start prcessing server=[%s]',server)
        top_consoleline = ''
        consoleline = ''
        pxe_ip_address = server_info[server]['MANAGEMENT_IP_V4']
        pxe_ip_gateway = server_info[server]['MANAGEMENT_GATEWAY_V4']
        pxe_ip_netmask = server_info[server]['MANAGEMENT_NETMASK_V4']
        pxe_file = str(server_info[server]['PXE_MAC'])
        pxe_file = re.sub(':','-',pxe_file)
        pxe_file = pxe_file.lower()
        ks_device = server_info[server]['PXE_DEVICE']
        web_ksfile = ks_http_location + '/' + server + '-ks.cfg'
        ksfile = scripts_path + '/' + server + '-ks.cfg'
        vmlinuz = server_info[server]['OS_VERSION'] + '-vmlinuz'

        if 'ubuntu' in server_info[server]['OS_VERSION']:
            initrd = server_info[server]['OS_VERSION'] + '-initrd.gz'
        else:
            initrd = server_info[server]['OS_VERSION'] + '-initrd.img'

        if (server_info[server]['CONSOLE_PORT']) == 2:
            top_consoleline = 'serial ' + str(server_info[server]['CONSOLE_PORT']) + ',' + str(server_info[server]['CONSOLE_SPEED'])
            consoleline = 'console=ttyS1,' + str(server_info[server]['CONSOLE_SPEED']) + ' console=tty'
        elif server_info[server]['CONSOLE_PORT'] == 1:
            top_consoleline = 'serial ' + str(server_info[server]['CONSOLE_PORT']) + ',' + str(server_info[server]['CONSOLE_SPEED'])
            consoleline = 'console=ttyS0,' + str(server_info[server]['CONSOLE_SPEED']) + ' console=tty'
        else:    
            top_consoleline = '#'
            consoleline = 'console=tty'

        pxe_file = tftpd_path + '/01-' + pxe_file
        copyfile(templates_path + '/template-pxe_file-' + server_info[server]['OS_VERSION'],pxe_file)
        for line in fileinput.input(pxe_file,inplace=1):
            if re.search('##TOPCONSOLELINE##',line):
                line = re.sub('##TOPCONSOLELINE##',top_consoleline,line)
            if re.search('##CONSOLELINE##',line):
                line = re.sub('##CONSOLELINE##',consoleline,line)
            if re.search('##PXE_MAC##',line):
                line = re.sub('##PXE_MAC##',server_info[server]['PXE_MAC'],line)
            if re.search('##PXE_DEVICE##',line):
                line = re.sub('##PXE_DEVICE##',server_info[server]['PXE_DEVICE'],line)
            if re.search('##VMLINUZ##',line):
                line = re.sub('##VMLINUZ##',vmlinuz,line)
            if re.search('##INITRD##',line):
                line = re.sub('##INITRD##',initrd,line)
            if re.search('##MANAGEMENT_IP_V4##',line):
                line = re.sub('##MANAGEMENT_IP_V4##',server_info[server]['MANAGEMENT_IP_V4'],line)
            if re.search('##MANAGEMENT_NETMASK_V4##',line):
                line = re.sub('##MANAGEMENT_NETMASK_V4##',server_info[server]['MANAGEMENT_NETMASK_V4'],line)
            if re.search('##MANAGEMENT_GATEWAY_V4##',line):
                line = re.sub('##MANAGEMENT_GATEWAY_V4##',server_info[server]['MANAGEMENT_GATEWAY_V4'],line)
            if re.search('##HOSTNAME##',line):
                line = re.sub('##HOSTNAME##',server,line)
            if re.search('##PXE_DNS##',line):
                line = re.sub('##PXE_DNS##',dns_nameserver,line)
            if re.search('##DOMAIN##',line):
                line = re.sub('##DOMAIN##',server_info[server]['DOMAIN'],line)
            if re.search('##KSFILE##',line):
                line = re.sub('##KSFILE##',web_ksfile,line)
            print(line,end='')

        dhcpd_hosts_file = global_info['DHCPD_PATH'] + '/dhcpd-kickstart-hosts.conf'
        fh = open(dhcpd_hosts_file,'a')
        fh.write('#\n# dhcp for ' + server + '\n#\n')
        fh.write('host ' + server + ' {\n')
        fh.write('    hardware ethernet ' + server_info[server]['PXE_MAC'] + ';\n')
        fh.write('    fixed-address ' + pxe_ip_address  + ';\n')
        fh.write('    option host-name "' + server  + '";\n')
        fh.write('    filename "prelinux.0";\n')
        fh.write('    next-server ' + global_info['TFTPD_IP'] + ';\n}\n#\n')
        fh.close()

        copyfile(templates_path + '/template-ks-' + server_info[server]['OS_VERSION'],ksfile)
        for line in fileinput.input(ksfile,inplace=1):
            if re.search('##HTTP_IP##',line):
                line = re.sub('##HTTP_IP##',global_info['HTTP_IP'],line)
            if re.search('##HTTP_TOP##',line):
                line = re.sub('##HTTP_TOP##',global_info['HTTP_TOP'],line)
            if re.search('##OS_VERSION##',line):
                line = re.sub('##OS_VERSION##',server_info[server]['OS_VERSION'],line)
            if re.search('##HOSTNAME##',line):
                line = re.sub('##HOSTNAME##',server,line)
            if re.search('##PXE_DNS##',line):
                line = re.sub('##PXE_DNS##',dns_nameserver,line)
            if re.search('##PXE_DEVICE##',line):
                line = re.sub('##PXE_DEVICE##',server_info[server]['PXE_DEVICE'],line)
            if re.search('##MANAGEMENT_IP_V4##',line):
                line = re.sub('##MANAGEMENT_IP_V4##',server_info[server]['MANAGEMENT_IP_V4'],line)
            if re.search('##MANAGEMENT_NETMASK_V4##',line):
                line = re.sub('##MANAGEMENT_NETMASK_V4##',server_info[server]['MANAGEMENT_NETMASK_V4'],line)
            if re.search('##MANAGEMENT_GATEWAY_V4##',line):
                line = re.sub('##MANAGEMENT_GATEWAY_V4##',server_info[server]['MANAGEMENT_GATEWAY_V4'],line)
            if re.search('##PXE_DNS##',line):
                line = re.sub('##PXE_DNS##',dns_nameserver,line)
            if re.search('##KEYBOARD##',line):
                line = re.sub('##KEYBOARD##',global_info['KEYBOARD'],line)
            if re.search('##TIMEZONE##',line):
                line = re.sub('##TIMEZONE##',global_info['TIMEZONE'],line)
            if re.search('##ROOT_PW##',line):
                line = re.sub('##ROOT_PW##',global_info['ROOT_PW'],line)
            if re.search('##SWAPSIZE##',line):
                line = re.sub('##SWAPSIZE##',str(server_info[server]['SWAPSIZE']),line)
            if re.search('##DRIVE##',line):
                line = re.sub('##DRIVE##',server_info[server]['DRIVE'],line)
            print(line,end='')
    logging.info('setup_servers completed')


def setup_servers_info(global_info,server_info):
    server_config_path = global_info['SCRIPTS_PATH']
    for key in server_info:
        fh = open(server_config_path + '/' + key + '-config.txt','w')
        for subkey in server_info[key]:
            fh.write(subkey +  '=' + str(server_info[key][subkey]) + '\n')
        fh.close()
    logging.info('setup_servers_info completed')


def setup_servers_scripts(global_info,server_info,network_info,network_v6_info):
    logging.info('setup_servers_scripts completed')

def restart_dhcp(KSparms,global_info):
    return
    if KSparms['LOCATION'] == 'TEST':
        logging.info('restart_dhchd TEST completed')
    elif KSparms['LOCATION'] == 'PRODUCTION':
        os.system("service isc-dhcp-server stop")
        os.system("service isc-dhcp-server start")
    logging.info('restart_dhchd completed')
