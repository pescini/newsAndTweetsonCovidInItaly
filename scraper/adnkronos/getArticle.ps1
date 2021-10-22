### SCRAPE FROM ADKRONOS

Get-ChildItem "CSV/" -filter *3.csv | Foreach-Object {
	$file = $_.Basename
	Write-Host "$file"
	
	Import-Csv  "CSV/$($_.Name)" -Delimiter ';' | Foreach-Object {
		$urlstr  = $_.url.Split("_")[1]
		$fname = "HTMLARTICLE/$($file)_$($urlstr).html"
		if (!(Test-Path $fname)){
			Invoke-WebRequest $_.url -OutFile $fname
		}
	}
	
	"url;body;quoted" | Out-File "CSVARTICLE/$($file).csv" -Encoding UTF8
	Get-ChildItem "HTMLARTICLE/" -Filter "$file*" | Foreach-Object {
		python html2txt.py -i "HTMLARTICLE/$($_.Name)"
		Get-Content .\temp.txt -Encoding UTF8 | Out-File "CSVARTICLE/$($file).csv" -Append -Encoding UTF8
	}
}
