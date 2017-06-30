<?php
session_start();

require("./lib/fortune.php");
include("./lib/db_func.php");
include("./config/config.inc.php");
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
include("./config/header.php");
$fortune_handle = new Fortune;
echo "<br><H1>The fortune of the moment is ..... </h1><br><br><br>";
$fortune_line = $fortune_handle->quoteFromDir("/usr/share/games/fortunes/");
echo "<h2>$fortune_line</h2>";
include("./config/footer.php");
?>
