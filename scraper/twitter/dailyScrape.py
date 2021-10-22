cli="""
Usage:
  scrape.py ( (-h | --help) | --version )
  scrape.py [-m=METHOD] [-l=NUM] [-r=NUM] [-o=FILE] [-s=DATE] [-u=DATE]

Options:
  -h --help  Show this screen.
  --version  Show version info.
  -s=DATE    Search start date [default: 2021-07-26]
  -u=DATE    Search end date [default: 2021-07-30]
  -r=RETRY   Times to retry query [default: 3]
  -m=METHOD  Get 'top' or 'live' results [default: top]
  -l=LIMIT   Maximum daily results [default: -1]
  -o=FILE    Output file [default: scrape.json]
"""
from docopt import docopt
from tqdm import tqdm
from snscrape.modules import twitter
from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

if __name__ == "__main__":
	args = docopt(cli, version='0.1')
	query = """
"prima ondata" OR "seconda ondata" OR "terza ondata" OR
"fase 1" OR "fase 2" OR "fase 3" OR "fase uno" OR "fase due" OR "fase tre"
OR "zona rossa" OR "zona arancione" OR "zona gialla" OR "zona bianca"
OR covid OR coronavirus OR virus OR pandemia OR tamponi OR
lockdown OR coprifuoco OR quarantena OR mascherina OR mascherine
OR variante OR varianti OR vaccino OR vaccini OR greenpass OR "green pass"
-filter:links -filter:replies lang:it
	""".replace("\n"," ").strip()
	for key in ("-r","-l"):
		args[key] = int(args[key])
	for key in ("-s","-u"):
		args[key] = date.fromisoformat(args[key])
	with open(args["-o"],"w") as f:
		for day in tqdm(daterange(args["-s"],args["-u"]),total=(args["-u"]-args["-s"]).days):
			#oldtweet=[0,0,0,0,0]
			k=0
			scraper = twitter.TwitterSearchScraper(
						"%s since:%s until:%s" % (query,day,day+timedelta(1)),
						top=args["-m"]!="live",retries=args["-r"])
			for i,tweet in tqdm(enumerate(scraper.get_items()),total=args["-l"]):
				#if tweet.id in oldtweet:
				#	break
				if args["-l"]!=-1 and i>args["-l"]:
					print("WARNING %s" % day)
					break
				
				f.write("\n")
				f.write(tweet.json())
				#oldtweet[k] = tweet.id
				#k = (k+1)%5 
