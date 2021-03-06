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
$table = $_REQUEST['table'];
if($table == 'system_ts')
{
   $system_id = 'system_ts_id';
   $system_attributes_table = 'system_ts_attributes';
   $system_notes_table = 'system_ts_notes';
}
elseif($table == 'system_ipmi')
{
   $system_id = 'system_ipmi_id';
   $system_attributes_table = 'system_ipmi_attributes';
   $system_notes_table = 'system_ipmi_notes';
}
$pgsqldb = new pgsql($endbhost,$endbname,$endbuser,$endbpass);
$pgsqldb->connect();
$pgsqldb->query("SELECT * FROM $table WHERE $system_id = $id"); 
$num_rows = $pgsqldb->numRows();
if($num_rows == 1)
{
   $row = $pgsqldb->fetchObject();
   echo "HOSTNAME = $row->hostname<br>\n";
   echo "CABINET = $row->system_row_number-$row->system_cabinet_number<br>\n";
   echo "UNIT NUMBER = $row->system_unit_number<br>\n";
   echo "SYSTEM TYPE = $row->system_type<br>\n";
   echo "SYSTEM SIZE = $row->system_unit_size<br>\n";
   echo "SYSTEM ASSET TAG = $row->att_tag<br>\n";
   echo "SYSTEM SERIAL NUMBER = $row->serial_number<br>\n";
   if($table == 'system_ts')
   {
      echo "SYSTEM TERMINAL SERVER = $row->system_ts<br>\n";
      echo "SYSTEM TERMINAL SERVER PORT = $row->system_tsport<br>\n";
      echo "SYSTEM POWER = $row->system_pwr<br>\n";
      echo "SYSTEM POWER PORT = $row->system_power_port<br>\n";
   }
   elseif($table == 'system_ipmi')
   {
      echo "SYSTEM OAM ADDRESS = $row->oam_ip_address<br>\n";
      echo "SYSTEM OAM DEVICE = $row->oam_device<br>\n";
      echo "SYSTEM IPMI ADDRESS = $row->ipmi_ip_address<br>\n";
   }
   echo "SYSTEM NETWORK = $row->system_network<br>\n";
   echo "PXE MAC = $row->pxe_mac<br>\n";
   echo "IP ADDRESS = $row->app_ip_address<br>\n";
   echo "IP DEVICE = $row->app_device<br>\n";
   echo "CONSOLE SPEED = $row->conspeed<br>\n";
   echo "CONSOLE PORT = $row->conport<br>\n";
   echo "IP BONDING = $row->bonding<br>\n";
   echo "SWAPSIZE = $row->swapsize<br>\n";
   echo "ARCH = $row->arch<br>\n";
   echo "APPLICATION TYPE = $row->type<br>\n";
   echo "OS = $row->server_os_version<br>\n";
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
