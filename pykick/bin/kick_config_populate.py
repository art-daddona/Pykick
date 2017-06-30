#!/usr/bin/python3
import sys
import os
import time
import logging
import re
import collections
import string
import psycopg2
sys.path.append('/home/art/work_stuff/pykick/lib')
from kicker_lib import *

def print_global(dbconn,global_fk,globalname,newglobalname):
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

    out_buffer = '[global=' + newglobalname + ']\nDHCPD_IP=' + dhcpd_ip + '\nDHCPD_PATH=' + dhcpd_path  + '\nTFTPD_IP=' + tftpd_ip
    print(out_buffer)
    out_buffer = 'TFTPD_PATH=' + tftpd_path + '\nHTTP_IP=' + http_ip + '\nHTTP_TOP=' + http_top + '\nOS_PATH=' + os_path + '\nSCRIPTS_PATH=' + scripts_path
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


def print_subnet():
    network_v4_name = 'management_vlan_506_v4'
    description = 'MANAGEMENT V4 NETWORK VLAN 506'
    network = '172.16.0.0'
    netmask = '255.255.254.0'
    router = '172.16.0.1'
    dhcp  = 1
    out_buffer = '[subnet_v4=' + network_v4_name + ']\nDESCRIPTION=' + description + '\nNETWORK=' + network 
    print(out_buffer,end='')
    out_buffer = '\nNETMASK=' + netmask + '\nROUTER=' + router + '\nDHCP=' + str(dhcp) + '\n'
    print(out_buffer)

    network_v4_name = 'management_vlan_507_v4'
    description = 'MANAGEMENT V4 NETWORK VLAN 507'
    network = '172.16.2.0'
    netmask = '255.255.254.0'
    router = '172.16.2.1'
    dhcp  = 1
    out_buffer = '[subnet_v4=' + network_v4_name + ']\nDESCRIPTION=' + description + '\nNETWORK=' + network 
    print(out_buffer,end='')
    out_buffer = '\nNETMASK=' + netmask + '\nROUTER=' + router + '\nDHCP=' + str(dhcp) + '\n'
    print(out_buffer)

    network_v4_name = 'application_vlan_2006_v4'
    description = 'APPLICATION V4 NETWORK VLAN 2006'
    network = '192.168.0.0'
    netmask = '255.255.254.0'
    router = '192.168.0.1'
    dhcp  = 0
    out_buffer = '[subnet_v4=' + network_v4_name + ']\nDESCRIPTION=' + description + '\nNETWORK=' + network 
    print(out_buffer,end='')
    out_buffer = '\nNETMASK=' + netmask + '\nROUTER=' + router + '\nDHCP=' + str(dhcp) + '\n'
    print(out_buffer)

    network_v4_name = 'application_vlan_2007_v4'
    description = 'APPLICATION V4 NETWORK VLAN 2007'
    network = '192.168.2.0'
    netmask = '255.255.254.0'
    router = '192.168.2.1'
    dhcp  = 0
    out_buffer = '[subnet_v4=' + network_v4_name + ']\nDESCRIPTION=' + description + '\nNETWORK=' + network 
    print(out_buffer,end='')
    out_buffer = '\nNETMASK=' + netmask + '\nROUTER=' + router + '\nDHCP=' + str(dhcp) + '\n'
    print(out_buffer)

    network_v6_name = 'management_vlan_506_v6'
    description = 'MANAGEMENT V6 NETWORK VLAN 506'
    network = '2016:1957:1890::'
    netmask = '64'
    router = '2016:1957:1890::1'
    dhcp  = 0
    out_buffer = '[subnet_v6=' + network_v6_name + ']\nDESCRIPTION=' + description + '\nNETWORK=' + network 
    print(out_buffer,end='')
    out_buffer = '\nNETMASK=' + netmask + '\nROUTER=' + router + '\nDHCP=' + str(dhcp) + '\n'
    print(out_buffer)

    network_v6_name = 'application_vlan_2006_v6'
    description = 'APPLICATION V6 NETWORK VLAN 2006'
    network = '2016:1957:1891::'
    netmask = '64'
    router = '2016:1957:1891::1'
    dhcp  = 0
    out_buffer = '[subnet_v6=' + network_v6_name + ']\nDESCRIPTION=' + description + '\nNETWORK=' + network 
    print(out_buffer,end='')
    out_buffer = '\nNETMASK=' + netmask + '\nROUTER=' + router + '\nDHCP=' + str(dhcp) + '\n'
    print(out_buffer)

def get_mac(num):
    mac = '00:00:00:00:00:00'
    n = int(mac.replace(':',''),16)
    n = n + num
    h = hex(n)
    newh = "{:012x}".format(n)
    mac = str(newh)
    blocks = [mac[x:x+2] for x in range(0,len(mac), 2)]
    mac_fixed = ':'.join(blocks)
    return(mac_fixed)

def print_server():
    # do 172.16.0.0/23
    for num in range(10,512):
        server = 'test_svr-' + str(num)
        os_version = 'ubuntu-14.04-x86_64'
        swapsize = 66000
        pxe_mac = get_mac(num)
        pxe_device = 'eth0'
        drive = 'sda'
        management_device = 'eth0'
        application_device = 'bond1:eth0,eth1'
        console_port = 0
        console_speed = 0
        system_type = '' 

        if(num < 256):
            management_ip_v4 = '172.16.0.' + str(num)
        else:
            management_ip_v4 = '172.16.1.' + str(num - 256)
        management_ip_v6 = 'none'
        if(num < 256):
            application_ip_v4  = '192.168.0.' + str(num)
        else:
            application_ip_v4  = '192.168.1.' + str(num - 256)
        application_ip_v6 = 'none'
        if num > 10 and num < 64:
            system_type = 'VBOX'
            console_port = 0
            console_speed = 0
            management_device = 'eth0'
            application_device = 'eth1'
            drive = 'sda'
            swapsize = 10000
        elif num > 64 and num < 81:
            system_type = 'OPENSTACK'
            console_port = 0
            console_speed = 0
            management_device = 'eth0'
            application_device = 'eth1'
            drive = 'vda'
            swapsize = 10000
        elif num > 80 and num < 97:
            system_type = 'BLADE HP G8'
            console_port = 2
            console_speed = 115200
            management_device = 'bond0:eth0,eth1'
            application_device = 'bond1:eth0,eth1'
            drive = 'sda'
            swapsize = 66000
        elif num > 97 and num < 513:
            system_type = 'RACK DELL R620'
            console_port = 2
            console_speed = 115200
            management_device = 'bond0:eth0,eth1'
            application_device = 'bond1:eth0,eth1'
            drive = 'sda'
            swapsize = 66000
        application_type = 'test'
        domain = 'kicker.com'
        status = 'KICK'
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
            print_server_virtual(server,num)
        elif 'RACK' in system_type:
            print_server_rack(server,num)
        elif 'BLADE' in system_type:
            print_server_blade(server,num)
        elif 'OPENSTACK' in system_type:
            print_server_openstack()
        out_buffer = '\n'
        print(out_buffer)

def print_server_virtual(server,num):
    vm_type = 'VBOX'
    vm_host = '10.18.10.10'
    vm_rdp_port = (7000 + num)
    vm_memory = 4096
    vm_cpu = 2
    vm_interface_device = 'bond0'
    vm_drive_type = 'ISCSI'
    vm_iscsi_target = '10.18.11.10'
    vm_iscsi_port = 3260
    vm_iscsi_iqn = 'iqn.2004-04.com.tester:myfileer-1:iscsi.' + server  + '.dec976'

    out_buffer = 'VM_TYPE=' + vm_type + '\nVM_HOST=' + vm_host + '\nVM_RDP_PORT=' + str(vm_rdp_port) + '\nVM_MEMORY=' + str(vm_memory)
    print(out_buffer)
    out_buffer = 'VM_CPU=' + str(vm_cpu) + '\nVM_INTERFACE_DEVICE=' + vm_interface_device + '\nVM_DRIVE_TYPE=' + vm_drive_type
    print(out_buffer)
    out_buffer = 'VM_ISCSI_TARGET=' + vm_iscsi_target + '\nVM_ISCSI_PORT=' + str(vm_iscsi_port) + '\nVM_ISCSI_IQN=' + vm_iscsi_iqn
    print(out_buffer)

def print_server_rack(server,num):
        if num < 256:
            rack_building = 'Test Center 1'
            rack_floor = 1
            rack_row = 500
        else:
            rack_building = 'Test Center 2'
            rack_floor = 12
            rack_row = 600
        rack_rack = (num % 7) + 1
        rack_unit = (num % 36) + 1
        rack_size = 1
        rack_serial = 'AGT786-' + str(num)
        if num < 256:
            rack_ipmi_ip_v4 = '10.10.0.' + str(num)
        else:
            rack_ipmi_ip_v4 = '10.10.1.' + str(num - 256)
        out_buffer = 'RACK_BUILDING=' + rack_building + '\nRACK_FLOOR=' + str(rack_floor) + '\nRACK_ROW=' + str(rack_row)
        print(out_buffer)
        out_buffer = 'RACK_RACK=' + str(rack_rack) + '\nRACK_UNIT=' + str(rack_unit) + '\nRACK_SIZE=' + str(rack_size) + '\nRACK_SERIAL=' + rack_serial 
        print(out_buffer)
        out_buffer = 'RACK_IPMI_IP_V4=' + rack_ipmi_ip_v4
        print(out_buffer)

def print_server_blade(server,num):
    blade_center = 101
    blade_unit = 10
    blade_serial = 'ABC123-' + str(num)
    blade_ip_v4 = '10.19.10.10'
    blade_ipmi_ip_v4 = '10.19.10.' + str(num)

    out_buffer = 'BLADE_CENTER=' + str(blade_center) + '\nBLADE_UNIT=' + str(blade_unit) + '\nBLADE_SERIAL=' + str( blade_serial)
    print(out_buffer)
    out_buffer = 'BLADE_IP_V4=' + blade_ip_v4 + '\nBLADE_IPMI_IP_V4=' + blade_ipmi_ip_v4
    print(out_buffer)

def print_server_openstack():
    openstack_url = 'http://horizon.kicker.com:5000/v2/'
    openstack_image = 'e3f77158-c626-4f61-8d3c-4c734baa2ece'
    flavor = 'ARTTEST'
    openstack_management_network = 'e3f77158-c626-4f61-8d3c-4c734baa2ece'
    openstack_application_network = 'e3f77158-c626-4f61-8d3c-4c734baa2ecc'
    openstack_ssh_key = 'art-key'
    openstack_security_group = 'default,art-sec-rules'
    openstack_zone = 'nova'

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
    logfile = '/home/art/work_stuff/pykick/logs/kick_config_populate.log'
    ks_parms = {}
    dbconn = ''
    globalname = ''
    global_fk = ''
 
    if len(sys.argv) != 3:
        print('Usage: kick_config_populate.py <CONFIG NAME> <NEW CONFIG NAME>')
        raise SystemExit(1)
    globalname = str(sys.argv[1])
    newglobalname = str(sys.argv[2])
    start_logging(logfile)
    get_ks_parms(configfile,ks_parms)
    dbconn = open_db(ks_parms)
    global_fk = get_global_fk(dbconn,globalname);
    if not global_fk:
        print('config name ',globalname,' is broken.... Usage: kick_config_populate.py <CONFIG NAME> <NEW CONFIG NAME>')
        close_db(dbconn)
        raise SystemExit(1)
    else:
        out_buffer = '#\n# global section for ' + newglobalname + '\n#\n'   
        print(out_buffer)
        print_global(dbconn,global_fk,globalname,newglobalname)
        out_buffer = '#\n# subnet section for ' + newglobalname + '\n#\n'   
        print(out_buffer)
        print_subnet()
        out_buffer = '#\n# server section for ' + newglobalname + '\n#\n'   
        print(out_buffer)
        print_server()
        close_db(dbconn)
        print('#kick_config_populate completed on config name ',newglobalname)
        raise SystemExit(1)
