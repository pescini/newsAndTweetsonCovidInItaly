$startDate = [DateTime]"2020-01-01"
$endDate   = [DateTime]"2021-08-01"

while($startDate -le $endDate) {
	$date = $startDate.ToString("yyMMdd")
	$files = [int](Get-ChildItem -Filter HTML/$($date)_*.html | Measure-Object).Count
	$file = 1
	
	"dailyRank;url;author;title;body;date;category" | Out-File "CSV/$($date).csv" -Encoding UTF8
	
	while($file -le $files){
		python html2csv.py -f "$($date)_$($file).html"
		Get-Content .\temp.csv -Encoding UTF8 | Out-File "CSV/$($date).csv" -Append -Encoding UTF8
		$file++
	}
	
	Write-Host $startDate.ToString("yyyy-MM-dd")
	$startDate = $startDate.AddDays(1)
}