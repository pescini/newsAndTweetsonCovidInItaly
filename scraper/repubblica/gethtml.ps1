$startDate = [DateTime]"2020-01-01"
$endDate   = [DateTime]"2021-08-01"

while($startDate -le $endDate) {
	$page = 1
	$pages = 0

	try{
		do{
			$query = "https://ricerca.repubblica.it/ricerca/repubblica-it?fromdate=$($startDate.ToString("yyyy-MM-dd"))&todate=$($startDate.ToString("yyyy-MM-dd"))&page=$page"
		
			Invoke-WebRequest $query -OutFile "HTML/$($startDate.ToString("yyMMdd"))_$page.html"
			
			if($pages -eq 0){
				$max = [string](Get-Content "HTML/$($startDate.ToString("yyMMdd"))_$page.html" | Select-String "<p>Pagina <strong>1</strong> di \d+</p>")
				$pages = [int]$max.Substring(33).Substring(0,$max.Length-37)
			}
			
			$page++
			#Start-Sleep 1
		}while($page -le $pages)
	}catch{
		Write-Host "ERROR $($startDate.ToString("yyyy-MM-dd"))"
		Start-Sleep 300
		#exit
	}
		
	Write-Host $startDate.ToString("yyyy-MM-dd")
	Start-Sleep 1
	$startDate = $startDate.AddDays(1)
}