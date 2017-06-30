<?php
session_start();

if(!isset($_REQUEST['viewrow']))
{
   header('Location: index.php');
   exit;
}

include("../config/config.inc.php");
include("../config/header.php");
include("../lib/db_func.php");

$dbrow = $_REQUEST['viewrow'];
$dbcab = $_REQUEST['viewcab'];

$pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
$pgsqldb->connect();
$pgsqldb->query("SELECT system_unit_number,system_unit_size,hostname FROM system_ts WHERE system_row_number = $dbrow AND system_cabinet_number = $dbcab UNION SELECT system_unit_number,system_unit_size,hostname FROM system_ipmi WHERE system_row_number = $dbrow AND system_cabinet_number = $dbcab ORDER BY system_unit_number DESC");
echo "<table class = \"rack_physical\" border=1>\n";
echo "<tr><th class=\"rack_header\" colspan=2>\n";
echo "CAB-$dbrow-$dbcab</th></tr>\n";

$rack_layout = array();
$system_size = array();

for($i = 1;$i < 43;$i++)
{
   $rack_layout[$i] = 'empty';
}
while($row = $pgsqldb->fetchObject())
{
   if($row->system_unit_size > 1)
   {
      for($i = $row->system_unit_number;$i < ($row->system_unit_number - 1) + $row->system_unit_size;$i++)
      {
         $rack_layout[$i] = 'full';
      }
      $rack_layout[$row->system_unit_number + ($row->system_unit_size - 1)] = $row->hostname;
      $system_size[$row->hostname] = $row->system_unit_size;
   }
   else
   {
      $rack_layout[$row->system_unit_number] = $row->hostname;
      $system_size[$row->hostname] = $row->system_unit_size;
   }
}

for($i = 42;$i > 0;$i--)
{
   echo "<tr><td class=\"rack_physical_num\">$i</td>\n";
   if($rack_layout[$i] == 'empty')
   {
      echo "<td rowspan=1 class=\"rack_physical_empty\">\n";
      echo "<span style=\"vertical-align: middle\"></span></td></tr>\n";
   }
   elseif($rack_layout[$i] == 'full')
   {
   }
   else 
   {
      $hostname = $rack_layout[$i];
      $rowspan = $system_size[$hostname];
      echo "<td rowspan=$rowspan class=\"rack_physical_dev\">\n";
      echo "<span style=\"vertical-align: middle\">\n";
      echo "<a class=\"racklayout\" title=\"View details for $rack_layout[$i]\" href=\"$url/html/detail_view.php?hostname=$rack_layout[$i]&row=$dbrow&cab=$dbcab\" <strong>$rack_layout[$i]</strong></a></td></tr>\n";
   }
}
echo "</table>\n";
include("../config/footer.php");
?>
