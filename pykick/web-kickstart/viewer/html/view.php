<?php

function load_buildings(&$db_rack_info,$gkey)
{
    include("../config/config.inc.php");
    $total_buildings = 0;
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    $pgsqldb->query("SELECT DISTINCT building from rack_info WHERE global_fk = $gkey");
    $num_rows = $pgsqldb->numRows();
    if($num_rows > 0)
    {
        while($row = $pgsqldb->fetchObject())
        {
            $db_rack_info[$total_buildings]['BUILDING'] = $row->building;
            $total_buildings++;
        }
    }
    return($total_buildings);
}

function load_blade_centers(&$db_blade_info,$gkey)
{
    include("../config/config.inc.php");
    $total_blade_centers = 0;
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    $pgsqldb->query("SELECT DISTINCT blade_center from blade_info WHERE global_fk = $gkey");
    $num_rows = $pgsqldb->numRows();
    if($num_rows > 0)
    {
        while($row = $pgsqldb->fetchObject())
        {
            $db_blade_info[$total_blade_centers]['BLADE_CENTER'] = $row->blade_center;
            $total_blade_centers++;
        }
    }
    return($total_blade_centers);
}

function load_vm_hosts(&$db_vm_info,$gkey)
{
    include("../config/config.inc.php");
    $total_vm_hosts = 0;
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    $pgsqldb->query("SELECT DISTINCT vm_host from vm_info WHERE global_fk = $gkey");
    $num_rows = $pgsqldb->numRows();
    if($num_rows > 0)
    {
        while($row = $pgsqldb->fetchObject())
        {
            $db_vm_info[$total_vm_hosts]['VM_HOST'] = $row->vm_host;
            $total_vm_hosts++;
        }
    }
    return($total_vm_hosts);
}

function load_openstack_urls(&$db_openstack_info,$gkey)
{
    include("../config/config.inc.php");
    $total_openstack_urls = 0;
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    $pgsqldb->query("SELECT DISTINCT openstack_url from openstack_info WHERE global_fk = $gkey");
    $num_rows = $pgsqldb->numRows();
    if($num_rows > 0)
    {
        while($row = $pgsqldb->fetchObject())
        {
            $db_openstack_info[$total_openstack_urls]['OPENSTACK_URL'] = $row->openstack_url;
            $total_openstack_urls++;
        }
    }
    return($total_openstack_urls);
}

function load_floors(&$db_rack_info,$gkey,$total_buildings)
{
    include("../config/config.inc.php");
    $total_floors = 0;
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    for($num = 0;$num < $total_buildings;$num++)
    {
        $building_name = $db_rack_info[$num]['BUILDING'];
        $pgsqldb->query("SELECT DISTINCT floor from rack_info WHERE global_fk = $gkey AND building = '$building_name' ORDER BY floor");
        $total_floors = 0;
        while($row = $pgsqldb->fetchObject())
        {
            $floor = $row->floor;
            $db_rack_info[$num]['FLOOR'][$total_floors] = $floor; 
            $total_floors++;
        }
    }
    return($total_floors);
}

function load_rows_racks(&$db_rack_info,$gkey,$total_buildings,$total_floors,&$total_racks)
{
    include("../config/config.inc.php");
    $total_rows = 0;
    $total_racks = 0;
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    for($building = 0;$building < $total_buildings;$building++ )
    {
        $building_name = $db_rack_info[$building]['BUILDING'];
        for($i = 0;$i < $total_floors;$i++) 
        {
            $info = $db_rack_info[$building]['FLOOR'][$i];
            $pgsqldb->query("SELECT DISTINCT row from rack_info WHERE global_fk = $gkey AND building = '$building_name' AND floor = $info ORDER BY row");
            $total_rows = 0;
            while($row = $pgsqldb->fetchObject())
            {
                $rack_row = $row->row;
                $db_rack_info[$building]['ROW'][$total_rows] = $rack_row; 
                $total_rows++;
                $total_racks = 0;
                $pgsqldb->query("SELECT DISTINCT rack from rack_info WHERE global_fk = $gkey AND building = '$building_name' AND floor = $info AND row = $rack_row ORDER BY rack");
                while($row_rack = $pgsqldb->fetchObject())
                {
                    $rack = $row_rack->rack;
                    $db_rack_info[$building]['RACK'][$total_racks] = $rack; 
                    $total_racks++;
                }
            }
        }
    }
    return($total_rows);
}

function get_hostname($gkey,$skey)
{
    include("../config/config.inc.php");
    $hostname = "";
    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
    $pgsqldb->connect();
    $pgsqldb->query("SELECT hostname from servers WHERE global_fk = $gkey AND server_fk = $skey");
    $row = $pgsqldb->fetchObject();
    $hostname = $row->hostname;
    return($hostname);
}

function print_rack_info($db_rack_info,$gkey,$gname,$total_buildings,$total_floors,$total_rows,$total_racks)
{
    include("../config/config.inc.php");
    for($i = 0;$i < $total_buildings;$i++)
    {
        $building_name = $db_rack_info[$i]['BUILDING'];
        for($j = 0;$j < $total_floors;$j++)
        {
            $floor = $db_rack_info[$i]['FLOOR'][$j];
            for($k = 0;$k < $total_rows;$k++)
            {
                $row = $db_rack_info[$i]['ROW'][$k];
                for($l = 0;$l < $total_racks;$l++)
                {
                    $rack = $db_rack_info[$i]['RACK'][$l];
                    echo "<table class = \"rack_physical\" border=1>\n";
                    echo "<tr><th class=\"rack_header\" colspan=3>\n";
                    echo "$building_name FLOOR: $floor ROW: $row RACK-$rack</th></tr>\n";
                    $rack_layout = array();
                    $system_info = array();
                    for($m = 1;$m < 43;$m++)
                    {
                       $rack_layout[$m] = 'empty';
                    }
                    $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
                    $pgsqldb->connect();
                    $pgsqldb->query("SELECT server_fk,unit,size,serial_number,ipmi_ip_v4 FROM rack_info WHERE global_fk = $gkey AND building = '$building_name' AND floor = $floor AND row = $row AND rack = $rack ORDER BY unit DESC");
                    while($rowin = $pgsqldb->fetchObject())
                    {
                        $server_fk = $rowin->server_fk;
                        $hostname = get_hostname($gkey,$server_fk);
                        if($rowin->size > 1)
                        {
                            for($n = $rowin->unit;$n < ($rowin->unit - 1) + $rowin->size;$n++)
                            {
                                $rack_layout[$n] = 'full';
                            }
                            $rack_layout[$rowin->unit + ($rowin->size - 1)] = $hostname;
                            $system_info[$hostname]['SIZE'] = $rowin->size;
                            $system_info[$hostname]['SERVER_FK'] = $server_fk;
                        }
                        else
                        {
                            $rack_layout[$rowin->unit] = $hostname;
                            $system_info[$hostname]['SIZE'] = $rowin->size;
                            $system_info[$hostname]['SERVER_FK'] = $server_fk;
                        }
                    }
                    for($p = 42;$p > 0;$p--)
                    {
                        echo "<tr><td class=\"rack_physical_num\">$p</td>\n";
                        if($rack_layout[$p] == 'empty')
                        {
                            echo "<td rowspan=1 class=\"rack_physical_empty\">\n";
                            echo "<span style=\"vertical-align: middle\"></span></td></tr>\n";
                        }
                        elseif($rack_layout[$p] == 'full')
                        {
                        }
                        else
                        {
                            $hostname = $rack_layout[$p];
                            $rowspan = $system_info[$hostname]['SIZE'];
                            $server_fk = $system_info[$hostname]['SERVER_FK'];
                            echo "<td rowspan=$rowspan class=\"rack_physical_dev\">\n";
                            echo "<span style=\"vertical-align: middle\">\n";
                            echo "<a class=\"racklayout\" title=\"View details for $rack_layout[$p]\" href=\"$url/html/detail_view.php?hostname=$hostname&skey=$server_fk&gkey=$gkey\" <strong>$rack_layout[$p]</strong></a></td></tr>\n";
                        }
                     }
                }
                echo "</table>\n"; 
                echo "<br>\n";
            }
        }
    }
}

function print_blade_info($db_blade_info,$gkey,$gname,$total_blade_centers)
{
    include("../config/config.inc.php");
    for($i = 0;$i < $total_blade_centers;$i++)
    {
        $blade_center = $db_blade_info[$i]['BLADE_CENTER'];
        $blade_count = 0;
        echo "<table class = \"rack_physical\" border=1>\n";
        echo "<tr><th class=\"rack_header\" colspan=3>\n";
        echo "BLADE CENTER: $blade_center</th></tr>\n";
        $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
        $pgsqldb->connect();
        $pgsqldb->query("SELECT count(*) from blade_info WHERE global_fk = $gkey and blade_center = $blade_center");
        $blade_count = $pgsqldb->numRows(); 
        $rack_layout = array();
        $system_info = array();
        for($j = 0;$j < 17;$j++)
        {
            $rack_layout[$j] = 'empty';
        }
        $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
        $pgsqldb->connect();
        $pgsqldb->query("SELECT server_fk,unit,serial_number,blade_center_ip_v4,ipmi_ip_v4 FROM blade_info WHERE global_fk = $gkey AND blade_center = $blade_center ORDER BY unit DESC");
        while($rowin = $pgsqldb->fetchObject())
        {
            $server_fk = $rowin->server_fk;
            $hostname = get_hostname($gkey,$server_fk);
            $rack_layout[$rowin->unit] = $hostname;
            $system_info[$hostname]['UNIT'] = $rowin->unit;
            $system_info[$hostname]['SERVER_FK'] = $server_fk;
        }
        for($l = 16;$l > 0;$l--)
        {
            echo "<tr><td class=\"rack_physical_num\">$l</td>\n";
            $hostname = $rack_layout[$l];
            $rowspan = 1;
            if($hostname != 'empty')
            {
                $server_fk = $system_info[$hostname]['SERVER_FK'];
            }
            echo "<td rowspan=$rowspan class=\"rack_physical_dev\">\n";
            echo "<span style=\"vertical-align: middle\">\n";
            if($hostname == 'empty')
            {
                echo "<a class=\"racklayout\" title=\"View details for $rack_layout[$l]\" <strong>$rack_layout[$l]</strong></a></td></tr>\n";
            }
            else
            {
                echo "<a class=\"racklayout\" title=\"View details for $rack_layout[$l]\" href=\"$url/html/detail_view.php?hostname=$hostname&skey=$server_fk&gkey=$gkey\" <strong>$rack_layout[$l]</strong></a></td></tr>\n";
            }
        }
        echo "</table>\n"; 
        echo "<br>\n";
    }
}

function print_vm_info($db_vm_info,$gkey,$gname,$total_vm_hosts)
{
    include("../config/config.inc.php");
    for($i = 0;$i < $total_vm_hosts;$i++)
    {
        $vm_host = $db_vm_info[$i]['VM_HOST'];
        $vm_count = 0;
        echo "<table class = \"rack_physical\" border=1>\n";
        echo "<tr><th class=\"rack_header\" colspan=3>\n";
        echo "VM  HOST: $vm_host</th></tr>\n";
        $rack_layout = array();
        $system_info = array();
        $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
        $pgsqldb->connect();
        $pgsqldb->query("SELECT server_fk FROM vm_info WHERE global_fk = $gkey AND vm_host = '$vm_host'");
        $row_count = $pgsqldb->numRows();
        for($j = 1;$j < $row_count;$j++)
        {
            $rack_layout[$j] = 'empty';
        }
        $unit = 1;
        while($rowin = $pgsqldb->fetchObject())
        {
            $server_fk = $rowin->server_fk;
            $hostname = get_hostname($gkey,$server_fk);
            $rack_layout[$unit] = $hostname;
            $system_info[$hostname]['SERVER_FK'] = $server_fk;
            $unit++;
        }
        for($l = $row_count;$l > 0;$l--)
        {
            echo "<tr><td class=\"rack_physical_num\">$l</td>\n";
            $hostname = $rack_layout[$l];
            $rowspan = 1;
            $server_fk = $system_info[$hostname]['SERVER_FK'];
            echo "<td rowspan=$rowspan class=\"rack_physical_dev\">\n";
            echo "<span style=\"vertical-align: middle\">\n";
            if($hostname == 'empty')
            {
                echo "<a class=\"racklayout\" title=\"View details for $rack_layout[$l]\" <strong>$rack_layout[$l]</strong></a></td></tr>\n";
            }
            else
            {
                echo "<a class=\"racklayout\" title=\"View details for $rack_layout[$l]\" href=\"$url/html/detail_view.php?hostname=$hostname&skey=$server_fk&gkey=$gkey\" <strong>$rack_layout[$l]</strong></a></td></tr>\n";
            }
        }
        echo "</table>\n";
        echo "<br>\n";
    }
}

function print_openstack_info($db_openstack_info,$gkey,$gname,$total_openstack_urls)
{
    include("../config/config.inc.php");
    for($i = 0;$i < $total_openstack_urls;$i++)
    {
        $openstack_url = $db_openstack_info[$i]['OPENSTACK_URL'];
        $url_count = 0;
        echo "<table class = \"rack_physical\" border=1>\n";
        echo "<tr><th class=\"rack_header\" colspan=3>\n";
        echo "OPENSTACK URL: $openstack_url</th></tr>\n";
        $rack_layout = array();
        $system_info = array();
        $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
        $pgsqldb->connect();
        $pgsqldb->query("SELECT server_fk FROM openstack_info WHERE global_fk = $gkey AND openstack_url = '$openstack_url'");
        $row_count = $pgsqldb->numRows();
        for($j = 1;$j < $row_count;$j++)
        {
            $rack_layout[$j] = 'empty';
        }
        $unit = 1;
        while($rowin = $pgsqldb->fetchObject())
        {
            $server_fk = $rowin->server_fk;
            $hostname = get_hostname($gkey,$server_fk);
            $rack_layout[$unit] = $hostname;
            $system_info[$hostname]['SERVER_FK'] = $server_fk;
            $unit++;
        }
        for($l = $row_count;$l > 0;$l--)
        {
            echo "<tr><td class=\"rack_physical_num\">$l</td>\n";
            $hostname = $rack_layout[$l];
            $rowspan = 1;
            $server_fk = $system_info[$hostname]['SERVER_FK'];
            echo "<td rowspan=$rowspan class=\"rack_physical_dev\">\n";
            echo "<span style=\"vertical-align: middle\">\n";
            if($hostname == 'empty')
            {
                echo "<a class=\"racklayout\" title=\"View details for $rack_layout[$l]\" <strong>$rack_layout[$l]</strong></a></td></tr>\n";
            }
            else
            {
                echo "<a class=\"racklayout\" title=\"View details for $rack_layout[$l]\" href=\"$url/html/detail_view.php?hostname=$hostname&skey=$server_fk&gkey=$gkey\" <strong>$rack_layout[$l]</strong></a></td></tr>\n";
            }
        }
        echo "</table>\n";
        echo "<br>\n";
    }
}

#
# MAIN
#

session_start();
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
if(!isset($_REQUEST['view']))
{
   header('Location: index.php');
   exit;
}
$gname = $_REQUEST['view'];
$gkey = $_REQUEST['viewkey'];


$total_buildings = 0;
$db_rack_info = array();

$total_buildings = load_buildings($db_rack_info,$gkey);
if($total_buildings > 0)
{
    $total_rows = 0;
    $total_cabinets = 0;
    $total_floors = 0;
    $total_rows = 0;
    $total_racks = 0;
    $total_floors = load_floors($db_rack_info,$gkey,$total_buildings);
    $total_rows = load_rows_racks($db_rack_info,$gkey,$total_buildings,$total_floors,$total_racks);
    print_rack_info($db_rack_info,$gkey,$gname,$total_buildings,$total_floors,$total_rows,$total_racks);
}

$total_blade_centers = 0;
$db_blade_info = array();

$total_blade_centers = load_blade_centers($db_blade_info,$gkey);
if($total_blade_centers > 0)
{
    print_blade_info($db_blade_info,$gkey,$gname,$total_blade_centers);
}

$total_vm_hosts = 0;
$db_vm_info = array();

$total_vm_hosts = load_vm_hosts($db_vm_info,$gkey);
if($total_vm_hosts > 0)
{
    print_vm_info($db_vm_info,$gkey,$gname,$total_vm_hosts);
}

$total_openstack_urls = 0;
$db_openstack_info = array();

$total_openstack_urls = load_openstack_urls($db_openstack_info,$gkey);
if($total_openstack_urls > 0)
{
    print_openstack_info($db_openstack_info,$gkey,$gname,$total_openstack_urls);
}

include("../config/footer.php");
?>
