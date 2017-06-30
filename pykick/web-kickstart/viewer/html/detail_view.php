<?php

function load_vm_info($skey,$gkey)
{
    include("../config/config.inc.php");
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    $pgsqldb->query("SELECT * FROM vm_info WHERE server_fk = $skey AND global_fk = $gkey"); 
    $row2 = $pgsqldb->fetchObject();
    echo "VM_TYPE = $row2->vm_type<br>\n";
    echo "VM_HOST = $row2->vm_host<br>\n";
    echo "VM_RDP_PORT = $row2->vm_rdp_port<br>\n";
    echo "VM_MEMORY = $row2->vm_memory<br>\n";
    echo "VM_CPU = $row2->vm_cpu<br>\n";
    echo "VM_INTERFACE_DEVICE = $row2->vm_interface_device<br>\n";
    echo "VM_DRIVE_TYPE = $row2->vm_drive_type<br>\n";
    echo "VM_ISCSI_TARGET = $row2->vm_iscsi_target<br>\n";
    echo "VM_ISCSI_PORT = $row2->vm_iscsi_port<br>\n";
    echo "VM_ISCSI_IQN = $row2->vm_iscsi_iqn<br>\n";
}

function load_rack_info($skey,$gkey)
{
    include("../config/config.inc.php");
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    $pgsqldb->query("SELECT * FROM rack_info WHERE server_fk = $skey and global_fk = $gkey"); 
    $row2 = $pgsqldb->fetchObject();
    echo "RACK_BUILDING = $row2->building<br>\n";
    echo "RACK_FLOOR = $row2->floor<br>\n";
    echo "RACK_ROW = $row2->row<br>\n";
    echo "RACK_RACK = $row2->rack<br>\n";
    echo "RACK_UNIT = $row2->unit<br>\n";
    echo "RACK_SIZE = $row2->size<br>\n";
    echo "RACK_SERIAL = $row2->serial_number<br>\n";
    echo "RACK_IPMI_IP_V4 = $row2->ipmi_ip_v4<br>\n";
}


function load_blade_info($skey,$gkey)
{
    include("../config/config.inc.php");
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    $pgsqldb->query("SELECT * FROM blade_info WHERE server_fk = $skey and global_fk = $gkey"); 
    $row2 = $pgsqldb->fetchObject();
    echo "BLADE_CENTER = $row2->blade_center<br>\n";
    echo "BLADE_UNIT = $row2->unit<br>\n";
    echo "BLADE_SERIAL = $row2->serial_number<br>\n";
    echo "BLADE_IP_V4 = $row2->blade_center_ip_v4<br>\n";
    echo "BLADE_IPMI_IP_V4 = $row2->ipmi_ip_v4<br>\n";
}

function load_openstack_info($skey,$gkey)
{
    include("../config/config.inc.php");
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    $pgsqldb->query("SELECT * FROM openstack_info WHERE server_fk = $skey and global_fk = $gkey"); 
    $row = $pgsqldb->fetchObject();
    echo "OPENSTACK_URL = $row->openstack_url<br>\n";
    echo "OPENSTACK_IMAGE = $row->image<br>\n";
    echo "OPENSTACK_FLAVOR = $row->flavor<br>\n";
    echo "OPENSTACK_MANAGEMENT_NETWORK = $row->management_network<br>\n";
    echo "OPENSTACK_APPLICATION_NETWORK = $row->application_network<br>\n";
    echo "OPENSTACK_SSH_KEY = $row->ssh_key<br>\n";
    echo "OPENSTACK_SECURITY_GROUP = $row->security_group<br>\n";
    echo "OPENSTACK_ZONE = $row->zone<br>\n";
}

session_start();
if(!isset($_REQUEST['hostname']))
{
   header('Location: index.php');
   exit;
}
include("../config/config.inc.php");
include("../lib/db_func.php");
$klistdb = new pgsql($dbhost,$dblist,$dbuser,$dbpass);
$klistdb->connect();
$klistdb->query("SELECT global_fk,global_name from listkickers");
$num = $klistdb->numRows();
if($num > 0)
{
    while($row = $klistdb->fetchObject())
    {
        $globalslist[$row->global_name] = $row->global_fk;
    }
}
include("../config/header.php");
$hostname = $_REQUEST['hostname'];
$skey = $_REQUEST['skey'];
$gkey = $_REQUEST['gkey'];

$pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
$pgsqldb->connect();
$pgsqldb->query("SELECT * FROM servers WHERE hostname = '$hostname' and server_fk = $skey and global_fk = $gkey"); 
$num_rows = $pgsqldb->numRows();
if($num_rows == 1)
{
   $row = $pgsqldb->fetchObject();
   echo "HOSTNAME = $row->hostname<br>\n";
   echo "OS_VERSION = $row->os_version<br>\n";
   echo "DRIVE = $row->drive<br>\n";
   echo "SWAP = $row->swap<br>\n";
   echo "CONSOLE_PORT = $row->console_port<br>\n";
   echo "CONSOLE_SPEED = $row->console_speed<br>\n";
   echo "PXE_MAC = $row->pxe_mac<br>\n";
   echo "PXE_DEVICE = $row->pxe_device<br>\n";
   echo "MANAGEMENT_DEVICE = $row->management_device<br>\n";
   echo "MANAGEMENT_IP_V4 = $row->management_ip_v4<br>\n";
   echo "MANAGEMENT_IP_V6 = $row->management_ip_v6<br>\n";
   echo "APPLICATION_DEVICE = $row->application_device<br>\n";
   echo "APPLICATION_IP_V4 = $row->application_ip_v4<br>\n";
   echo "APPLICATION_IP_V6 = $row->application_ip_v6<br>\n";
   echo "DOMAIN = $row->domain<br>\n";
   echo "APPLICATION_TYPE = $row->application_type<br>\n";
   echo "SYSTEM_TYPE = $row->system_type<br>\n";
   echo "STATUS = $row->status<br>\n";
   if($row->system_type == 'VBOX')
   {
       load_vm_info($skey,$gkey);
   }
   else if(strstr($row->system_type,'RACK '))
   {
       load_rack_info($skey,$gkey);
   }
   else if(strstr($row->system_type,'BLADE ')) 
   {
       load_blade_info($skey,$gkey);
   }
   else if($row->system_type == 'OPENSTACK') 
   {
       load_openstack_info($skey,$gkey);
   }
   echo "<br><br>\n";
}
else
{
}
include("../config/footer.php");
?>
