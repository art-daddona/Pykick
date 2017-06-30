<?php
include("../lib/db_func.php");

$dbname = "kicker";
$dblist = "kickerlist";
$dbhost = "127.0.0.1";
$dbuser = "art";
$dbpass = "0u8me2";
$title = "Rack View";
$url = "http://127.0.0.1/viewer";
$adminer_url = "http://127.0.0.1/phppgadmin/index.php";

$klistdb = new pgsql($dbhost,$dblist,$dbuser,$dbpass);
$klistdb->connect();
$klistdb->query("SELECT global_fk,global_name from listkickers");
$num = $klistdb->numRows();
if($num > 0)
{
    $globals = array();
    while($row = $klistdb->fetchObject())
    {
        $globals[$row->global_name] = $row->global_fk;
    }
}
print_r($globals);

?>
