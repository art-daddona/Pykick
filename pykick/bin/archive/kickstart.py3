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
#START get_broadcast returns ipv4 broadcast address
#
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

#
#END get_broadcast
#

#
#START get_network returns ipv4 network address
#
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

#
#END get_network
#

#
#START get_network_v6 returns ipv6 network address
#
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

#
#END get_network_v6
#

#
#START get_subnet_network returns ipv4 subnet address
#
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

#
#END get_subnet_network
#

#
#START get_subnet_network_v6 returns ipv6 subnet address
#
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

#
#END get_subnet_network_v6
#

#
#START get_router returns ipv4 gateway address
#
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

#
#END get_router
#

#
#START get_router_v6 returns ipv6 gateway address
#
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

#
#END get_router_v6
#

#
#START get_netmask returns ipv4 netmask
#
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

#
#END get_netmask
#

#
#START get_netmask_v6 returns ipv6 netmask
#
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

#
#END get_netmask_v6
#


#
#START read_config
#
def read_config(dbconn,global_fk,global_info,network_info,network_v6_info,server_info):
    global_name = ''
    network_name = ''
    network_v6_name = ''
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
        server = key
        server_fk,server_info[key]['HOSTNAME'],server_info[key]['OS_VERSION'],server_info[key]['DRIVE'],server_info[key]['SWAPSIZE'],server_info[key]['CONSOLE_PORT'],server_info[key]['CONSOLE_SPEED'],server_info[key]['PXE_MAC'],server_info[key]['PXE_DEVICE'],server_info[key]['MANAGEMENT_DEVICE'],server_info[key]['MANAGEMENT_IP_V4'],server_info[key]['MANAGEMENT_IP_V6'],server_info[key]['APPLICATION_DEVICE'],server_info[key]['APPLICATION_IP_V4'],server_info[key]['APPLICATION_IP_V6'],server_info[key]['SYSTEM_TYPE'],server_info[key]['APPLICATION_TYPE'],server_info[key]['DOMAIN'],server_info[key]['STATUS'] = row
        if server_info[key]['SYSTEM_TYPE'] == 'VBOX':
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
        elif 'RACK' in server_info[key]['SYSTEM_TYPE']:
            sql = 'SELECT building,floor,row,rack,unit,size,serial_number,ipmi_ip_v4 from rack_info WHERE global_fk = %s AND server_fk = %s;'
            sql_data = (global_fk,server_fk,)
            cur = dbconn.cursor()
            cur.execute(sql,sql_data)
            rows = cur.fetchone()
            cur.close()
            if not len(rows):
                out_buffer = 'ERROR reading database table rack_info for server [' + server + ']'
                print(out_buffer)
            server_info[server]['RACK_BUILDING'],server_info[server]['RACK_FLOOR'],server_info[server]['RACK_ROW'],server_info[server]['RACK_RACK'],server_info[server]['RACK_UNIT'],server_info[server]['RACK_SIZE'],server_info[server]['RACK_SERIAL'],server_info[server]['RACK_IPMI_IP_V4'] = rows
        elif 'BLADE' in server_info[key]['SYSTEM_TYPE']:
            sql = 'SELECT blade_center,unit,serial_number,blade_center_ip_v4,ipmi_ip_v4 from blade_info WHERE global_fk = %s AND server_fk = %s;'
            sql_data = (global_fk,server_fk,)
            cur = dbconn.cursor()
            cur.execute(sql,sql_data)
            rows = cur.fetchone()
            cur.close()
            if not len(rows):
                out_buffer = 'ERROR reading database table blade_info for server [' + server + ']'
                print(out_buffer)
            server_info[server]['BLADE_CENTER'],server_info[server]['BLADE_UNIT'],server_info[server]['BLADE_SERIAL'],server_info[server]['BLADE_IP_V4'],server_info[server]['BLADE_IPMI_IP_V4'] = rows
        elif 'OPENSTACK' in server_info[key]['SYSTEM_TYPE']:
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
    logging.info('read_config completed')
    return(1)
#
#END read_config
#

#
#START print_config
#
def print_config(global_info,network_info,network_v6_info,server_info):
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

#
#END print_config
#

#
#START check_server_network
#   
def check_server_network(global_info,server_info,network_info,network_v6_info,config_name):
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

#
#END check_server_network
#   

#
#START setup_dhcp
#   
def setup_dhcp(global_info,network_info,KSparms):
    domains = global_info['SEARCH_DOMAINS']
    domains = re.sub('[,]',' ',domains)
    dns_servers = global_info['DNS_SERVERS']    
    location = ksparms['LOCATION']

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
#
#END setup_dhcp
#   

#
#START setup_tftpd
#   
def setup_tftpd(global_info,ksparms):
    import glob

    location = ksparms['LOCATION']
    tftpd_dir = global_info['TFTPD_PATH']

    tftpd_dir = tftpd_dir + '/pxelinux.cfg/'
    os.chdir(tftpd_dir)
    tftpd_files =  glob.glob('01-*')
    for filename in tftpd_files:
        logging.info('setup_tftpd unlink %s/%s',tftpd_dir,filename)
        os.unlink(filename)
    logging.info('setup_tftpd completed')
#
#END setup_tftpd
#   

#
#START setup_servers
#   
def setup_servers(global_info,network_info,server_info,ksparms):
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
                line = re.sub('##INITRD##',vmlinuz,line)
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

#
#END setup_servers
#   

#
#START setup_servers_info
#   
def setup_servers_info(global_info,server_info):
    server_config_path = global_info['SCRIPTS_PATH']

    for key in server_info:
        fh = open(server_config_path + '/' + key + '-config.txt','w')
        for subkey in server_info[key]:
            fh.write(subkey +  '=' + str(server_info[key][subkey]) + '\n')

        fh.close()

    logging.info('setup_servers_info completed')
        
#
#END setup_servers_info
#   


#START setup_servers_scripts
#   
def setup_servers_scripts(global_info,server_info,network_info,network_v6_info):
    logging.info('setup_servers_scripts completed')
#
#END setup_servers_scripts
#

#
#START restart_dhcpd
#

def restart_dhcp(KSparms,global_info):
    return
    if KSparms['LOCATION'] == 'TEST':
        logging.info('restart_dhchd TEST completed')
    elif KSparms['LOCATION'] == 'PRODUCTION':
        os.system("service isc-dhcp-server stop")
        os.system("service isc-dhcp-server start")
    logging.info('restart_dhchd completed')

#
#END restart_dhcpd
#

#
# MAIN
#

if __name__ == '__main__':

    ksconfigfile = '/home/art/work_stuff/pykick/config/kickstart.config'
    logfile = '/home/art/work_stuff/pykick/logs/kickstart.log'
    ksparms = {}
    configname = ''
    global_info = {}
    network_info = collections.defaultdict(dict)
    network_v6_info = collections.defaultdict(dict)
    server_info = collections.defaultdict(dict)

    if len(sys.argv) != 2:
        print('Usage: kickstart.py3 <GLOBAL_NAME>')
        raise SystemExit(1)
    start_logging()
    get_ks_parms(ksparms,ksconfigfile)
    dbconn = open_db(ksparms)

    configname = str(sys.argv[1])
    global_fk = get_global_fk(configname)
    if global_fk:
        logging.info('global name [%s] good....so continue',configname)
        read_config(dbconn,global_fk,global_info,network_info,network_v6_info,server_info)
        print_config(global_info,network_info,network_v6_info,server_info)
        check_server_network(global_info,server_info,network_info,network_v6_info,configname)
        setup_dhcp(global_info,network_info,ksparms)
        setup_tftpd(global_info,ksparms)
        setup_servers(global_info,network_info,server_info,ksparms)
        setup_servers_info(global_info,server_info)
        setup_servers_scripts(global_info,server_info,network_info,network_v6_info)
        restart_dhcp(ksparms,global_info)
        print('kickstart.py has completed. Logfile is ',logfile)
        raise SystemExit(1)
    else:
        logging.info('Config Name [%s] invalid....so exit',configname)
        print('Config Name [',configname,'] invalid....so exit')
        raise SystemExit(1)
