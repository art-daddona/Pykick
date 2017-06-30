<?php
session_start();

if(!isset($_REQUEST['view']))
{
   header('Location: index.php');
   exit;
}

include("../config/config.inc.php");
include("../config/header.php");
include("../lib/db_func.php");

$mc_view = $_REQUEST['view'];
$dcl_mc = $_REQUEST['dclview'];

$total_cabinets = 0;
$pgsqldb = new pgsql($endbhost,$endbname,$endbuser,$endbpass);
$pgsqldb->connect();

if($mc_view == 'cabinet')
{
   $pgsqldb->query("SELECT system_row_number,system_cabinet_number from system_ts UNION select system_row_number,system_cabinet_number from system_ipmi");
   $num_rows = $pgsqldb->numRows();
   if($num_rows > 0)
   {
      while($row = $pgsqldb->fetchObject())
         echo "<a href=\"$url/html/encore_cabinet_view.php?viewrow=$row->system_row_number&viewcab=$row->system_cabinet_number\">CABINET $row->system_row_number - $row->system_cabinet_number</a><br>\n";
   }

}
else
{
   $pgsqldb->query("SELECT system_row_number,system_cabinet_number from system_ts WHERE mc = '$mc_view' OR mc = '$dcl_mc' UNION select system_row_number,system_cabinet_number from system_ipmi WHERE mc = '$mc_view' OR mc = '$dcl_mc'");
   $num_rows = $pgsqldb->numRows();
   if($num_rows > 0)
   {
      $total_cabinets = $num_rows;
      $dbrow = array();
      $dbcab = array();
      while($row = $pgsqldb->fetchObject())
      {
         $dbrow[] = $row->system_row_number;
         $dbcab[] = $row->system_cabinet_number;
      }
      for($c = 0;$c < $total_cabinets;$c++)
      {
         $pgsqldb->query("SELECT system_unit_number,system_unit_size,hostname,mc FROM system_ts WHERE system_row_number = $dbrow[$c] AND system_cabinet_number = $dbcab[$c] UNION SELECT system_unit_number,system_unit_size,hostname,mc FROM system_ipmi WHERE system_row_number = $dbrow[$c] AND system_cabinet_number = $dbcab[$c] ORDER BY system_unit_number DESC");
         echo "<table class = \"rack_physical\" border=1>\n";
         echo "<tr><th class=\"rack_header\" colspan=3>\n";
         echo "CAB-$dbrow[$c]-$dbcab[$c]</th></tr>\n";
         $rack_layout = array();
         $system_size = array();
         $system_mc = array();
         $cisco_cab = 0;
         if($dbrow[$c] == 601 && $dbcab[$c] < 8)
         {
            $cisco_cab = 1;
         }
         for($i = 1;$i < 43;$i++)
         {
            $rack_layout[$i] = 'empty';
         }
         while($row = $pgsqldb->fetchObject())
         {
            if($row->system_unit_size > 1)
            {
               if($cisco_cab)
               {
                  $rack_layout[$row->system_unit_number ] = $row->hostname;
                  $system_size[$row->hostname] = $row->system_unit_size;
                  $system_mc[$row->hostname] = $row->mc;
                  for($i = $row->system_unit_number + 1;$i <= $row->system_unit_number + $row->system_unit_size;$i++)
                  {
                     $rack_layout[$i] = 'full';
                  }
               }
               else
               {
                  for($i = $row->system_unit_number;$i < ($row->system_unit_number - 1) + $row->system_unit_size;$i++)
                  {
                     $rack_layout[$i] = 'full';
                  }
                  $rack_layout[$row->system_unit_number + ($row->system_unit_size - 1)] = $row->hostname;
                  $system_size[$row->hostname] = $row->system_unit_size;
                  $system_mc[$row->hostname] = $row->mc;
               }
            }
            else
            {
               $rack_layout[$row->system_unit_number] = $row->hostname;
               $system_size[$row->hostname] = $row->system_unit_size;
               $system_mc[$row->hostname] = $row->mc;
            }
         }

         if($cisco_cab)
         {
            for($i = 1;$i < 43;$i++)
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
                  echo "<a class=\"racklayout\" title=\"View details for $rack_layout[$i]\" href=\"$url/html/encore_detail_view.php?hostname=$rack_layout[$i]&row=$dbrow[$c]&cab=$dbcab[$c]\" <strong>$rack_layout[$i]</strong></a></td><td rowspan=$rowspan class=\"rack_physical_num\"><span style=\"vertical-align: left\">MC = $system_mc[$hostname]</td></tr>\n";
               }
            }
         }
         else
         {
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
                  echo "<a class=\"racklayout\" title=\"View details for $rack_layout[$i]\" href=\"$url/html/encore_detail_view.php?hostname=$rack_layout[$i]&row=$dbrow[$c]&cab=$dbcab[$c]\" <strong>$rack_layout[$i]</strong></a></td><td rowspan=$rowspan class=\"rack_physical_num\"><span style=\"vertical-align: left\">MC = $system_mc[$hostname]</td></tr>\n";
               }
            }
         }
         echo "</table>\n";
      }
   }
}
include("../config/footer.php");
?>
