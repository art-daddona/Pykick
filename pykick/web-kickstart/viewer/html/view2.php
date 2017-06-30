
<?php
session_start();

//if(!isset($_REQUEST['view']))
//{
//   header('Location: index.php');
//   exit;
/}

include("../config/config.inc.php");
include("../config/header.php");
include("../lib/db_func.php");

$search_type = $_REQUEST['view'];

if($search_type == "enc01")
{
   $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
   $pgsqldb->connect();
   $pagesize = 5;
   $recordstart = (isset($_GET['recordstart'])) ? $_GET['recordstart'] : 0;
   $pgsqldb->query("SELECT row,cabinet,unit_number,hostname FROM enc01 ORDER by row,cabinet,unit_number LIMIT $pagesize OFFSET $recordstart");
   echo $pgsqldb->getResultAsTable();
   $pgsqldb->query("SELECT count(*) from enc01");
   $row = $pgsqldb->fetchObject();
   $totalrows = $row->count;
   if($recordstart > 0)
   {
      $prev = $recordstart - $pagesize;
      $url = $_SERVER['PHP_SELF']."?recordstart=$prev";
      echo "<a href=\"$url\">Previous Page</a> ";
   }
   if($totalrows > ($recordstart + $pagesize))
   {
      $next = $recordstart + $pagesize;
      $url = $_SERVER['PHP_SELF']."?recordstart=$next";
      echo "<a href=\"$url\">Next Page</a> ";
   }
}
elseif($search_type == "enc02")
{
   $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
   $pgsqldb->connect();
   $pgsqldb->query("SELECT * FROM enc02 ORDER by row,cabinet,unit_number");
   echo $pgsqldb->getResultAsTable();
}
elseif($search_type == "enc03")
{
   $pgsqldb = new pgsql($dbhost,$dbname,$dbuser,$dbpass);
   $pgsqldb->connect();
   $pgsqldb->query("SELECT * FROM enc03 ORDER by row,cabinet,unit_number");
   echo $pgsqldb->getResultAsTable();
}
else
{
}
include("../config/footer.php");
?>
