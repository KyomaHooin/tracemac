<html>
<body>
<img src="logo.png">
<br><br>
<form method="get" action="index.php">
<table border="1" style="border-width: 1px;border-spacing: 2px;border-collapse: collapse;">
<tr><td>
<table border="0" cellpadding="5" style="border-width: 1px;border-spacing: 2px;border-collapse: collapse;">
<tr>
<td><input type="" name="mac"></td>
<td><input type="submit" value="vyhledat"/></td>
</tr>
</table>
</td></tr>
</table>
</form>

<?php

$map = "map.txt";
$hex = "[0-9A-Fa-f][0-9A-Fa-f]";

#MAC pattern filter
$win_linux ="/($hex([:-])$hex(\\2$hex){4})/";
$hex_only = "(($hex){6})";
$cisco = "(($hex$hex.){2}$hex$hex)";

# Check if we have MAP data
if (file_exists($map)) {
	# MAC regexp match
	if(strlen($_GET["mac"]) !== 0) {
		# linux, M$ DHCP, hex, cisco MAC style
		if ( preg_match($win_linux,$_GET["mac"]) or preg_match("/($hex_only|$cisco)/",$_GET["mac"]) ) {
			#create MAC hex 
			$mac ='0x' . strtolower(str_replace(array('-',':','.'),'',$_GET["mac"]));
			#Open MAP file
			$file = @fopen($map,'r');
			if ($file) {
				#Loop through each line
   				while (($line = fgets($file)) !== false) {
					#split the line
					$split = explode(';',$line);
					#search for match
       					if ( $mac == $split[1] ) {
						echo "<font size=2><b>IP: </b>$split[0]<br><b>MAC: </b>$split[1]<br><b>PORT: </b>$split[2]<br><br></font>";
					}
  				}
			#Close MAP file
    			fclose($file);
			}
		} else { echo '<font size=2><b>Bad mac ..</b></font>'; }
	}
} else { echo '<b>No map.txt file ..</b>'; }

?>

</body>
</html>
