$startDate = [DateTime]"2020-01-01"
$endDate   = [DateTime]"2021-08-01"

while($startDate -le $endDate) {
	$max = [string](Get-Content "HTML/$($startDate.ToString("yyMMdd"))_1.html" | Select-String "La ricerca ha prodotto <strong>\d+</strong> risultati per il termine")
	$real = [int]$max.Substring(61).Split("<")[0]

	if($real -ne ((Get-Content CSV/$($startDate.ToString("yyMMdd")).csv).Length-1)){
		Write-Host $($startDate.ToString("yyyy-MM-dd"))
	}
	$startDate = $startDate.AddDays(1)
}