<?php
define("hijau","\e[32m");
define("merah","\e[31m");
define("biru","\e[1;34m");
define('kuning',"\e[1;33m");
	class PhpUnit{
		public function Save($save,$name){
			$result = fopen($name, "a+");
			fwrite($result, "$save\n");
			fclose($result);
		}
		public function MassLaravel($asu){
			$fuck = "http://".$asu;
			$list = "https://raw.githubusercontent.com/dmzhari/bruteforce-lists/master/phpunit.txt"; // List Path Of Laravel phpunit
			$phpunit = file_get_contents($list); // Get file from url
			$exp = explode("\n", $phpunit);
			foreach ($exp as $key) {
				for($i = 0; $i < $key;$i++);
				$web = $fuck.$key;
				$stri = get_headers($web);
       			$cek =  $stri[0];
       			if(strpos($cek,"200")){
					echo hijau."[+] Found => $web\n";
					$found = "[+] URL : $web\n";
					$this->Save($found,"result.txt");
				}
				else{
					echo merah."Not Found => $web\n";
				}
			}
		}
		public function Laravel($asu){
			$fuck = "http://".$asu;
			$list = "https://raw.githubusercontent.com/dmzhari/bruteforce-lists/master/phpunit.txt"; // List Path Of Laravel phpunit
			$phpunit = file_get_contents($list); // Get file from url
			$exp = explode("\n", $phpunit);
			foreach ($exp as $key) {
				$web = $fuck.$key;
				$stri = get_headers($web);
       			$cek =  $stri[0];
       			if(strpos($cek,"200")){
					echo hijau."[+] Found => $web\n";
					$found = "[+] URL : $web\n";
					$this->Save($found,"result.txt");
				}
				else{
					echo merah."Not Found => $web\n";
				}
			}
		}
		public function Pilih(){
			echo hijau."\n\t<!>Scan Laravel Phpunit Coded By .LAKER<!>\n";
			echo merah."\nNote : Don't Change http:// Or https://\n";
			echo biru."1. Mass Scan Laravel Phpunit\n";
			echo kuning."2. Scan Laravel Phpunit No Mass\n\n";
			echo merah."Chose Your 1/2 => ";
			$pilih = trim(fgets(STDIN));
			switch ($pilih) {
				case '1':
					echo hijau."Your List site => ";
					$our = trim(fgets(STDIN));
					if(!file_exists($our)) die("File List ".$our." Not Found");
					$domain =  explode("\n", file_get_contents($our));
					foreach ($domain as $env) {
						$this->MassLaravel($env);
					}
					break;
				case '2':
					echo hijau."Your Site => ";
					$our = trim(fgets(STDIN));
					$this->Laravel($our);
				break;
				default:
					echo "\n\tWhat happened??\n";
					break;
			}
		}
	}
	$phpunit = new PhpUnit();
	$phpunit->Pilih();
?>
