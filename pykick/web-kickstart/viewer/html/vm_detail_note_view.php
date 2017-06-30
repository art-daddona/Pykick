<?php

session_start();
if(!isset($_REQUEST['id']))
{
   header('Location: index.php');
   exit;
}
include("../config/config.inc.php");
include("../config/header.php");
include("../lib/db_func.php");

$id = $_REQUEST['id'];
$system_id = 'system_vm_id';
$system_attributes_table = 'system_vm_attributes';
$system_notes_table = 'system_vm_notes';
$pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
$pgsqldb->connect();
$pgsqldb->query("SELECT * FROM system_vm  WHERE $system_id = $id"); 
$num_rows = $pgsqldb->numRows();
if($num_rows == 1)
{
   $row = $pgsqldb->fetchObject();
   echo "HOSTNAME = $row->hostname<br>\n";
   echo "IP ADDRESS = $row->app_ip_address<br>\n";
   echo "IP DEVICE = $row->app_device<br>\n";
   echo "VMHOST = $row->system_vm_host<br>\n";
   echo "VM_PORT = $row->system_vm_port<br>\n";
   echo "SYSTEM TYPE = VM GUEST<br>\n";
   echo "PXE MAC = $row->pxe_mac<br>\n";
   echo "IP BONDING = $row->bonding<br>\n";
   echo "SWAPSIZE = $row->swapsize<br>\n";
   echo "ARCH = $row->arch<br>\n";
   echo "OS = $row->server_os_version<br>\n";
   echo "APPLICATION TYPE = $row->type<br>\n";
   echo "LABS VERSION = $row->server_um_version<br>\n";
   echo "DCL VERSION = $row->server_dcl_version<br>\n";
   echo "DOMAIN = $row->domain<br>\n";
   echo "MC = $row->mc<br>\n";
   $pgsqldb->query("SELECT * FROM $system_attributes_table WHERE $system_id = $id");
   while($row = $pgsqldb->fetchObject())
   {
      echo "$row->attribute = $row->value<br>\n";
   }
   $pgsqldb->query("SELECT * FROM $system_notes_table WHERE $system_id = $id");
   echo "<br><br><br>NOTES<br><br>\n";
   while($row = $pgsqldb->fetchObject())
   {
      echo "$row->note_timestamp = $row->note<br>\n";
   }
}
include("../config/footer.php");
?>
