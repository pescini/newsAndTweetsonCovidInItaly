param($query, $outfile="temp", $startDate="2020-01-01", $endDate="2021-08-01")

### SCRAPE FROM ADKRONOS

$startDate = [DateTime]$startDate
$endDate   = [DateTime]$endDate

$page = 1
$pages = 0

if($query -eq "Giorgio Palu"){
	$query = "Giorgio Palù"
}

Write-Host "QUERY: $query - FILE: $outfile"

do{
	$request = "https://www.adnkronos.com/search?query=`"$query`"&startDate=$($startDate.toString("yyyy-MM-ddT00:00:00"))&endDate=$($endDate.toString("yyyy-MM-ddT00:00:00"))&page=$page"
	try{
		Invoke-WebRequest $request -OutFile "HTML/$($outfile)_$($page).html"
	}catch{
		$page--
		Write-Host "ERROR: TOO MANY REQUESTS"
		Start-Sleep 100
	}
	
	if($pages -eq 0){
		try{
			$pages = [int]([string](Get-Content "HTML/$($outfile)_1.html" | Select-String "TOTPGS: +\d+")).Substring(8)
			if($pages -gt 20){
				$pages = 20
				Write-Host "WARNING: LIMITED RESULTS"
			}
		}catch{
			$page--
			Write-Host "ERROR: NO RESULTS"
			Exit 1
		}
	}
	
	$page++
	#Start-Sleep 1
	
}while($page -le $pages)

### CONVERT TO CSV

$files = [int](Get-ChildItem -Filter HTML/$outfile*.html | Measure-Object).Count
$file = 1

"expert;date;time;url;title" | Out-File "CSV/$($outfile).csv" -Encoding UTF8

while($file -le $files){
	python html2csv.py -i "$($outfile)_$($file).html"
	Get-Content .\temp.csv -Encoding UTF8 | Out-File "CSV/$($outfile).csv" -Append -Encoding UTF8
	$file++
}
