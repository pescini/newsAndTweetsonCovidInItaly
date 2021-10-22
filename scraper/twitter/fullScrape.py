cli="""
Usage:
  scrape.py (-h | --help)
  scrape.py --version
  scrape.py [-q=<query>] [-m=<method>] [-l=<limit>] [-r=<retry>] [-o=<output>]

Options:
  -h --help    Show this screen.
  --version    Show version info.
  -q=<query>   Search query [default: ""]
  -r=<retry>   Times to retry query [default: 3]
  -m=<method>  Get 'top' or 'live' results [default: live]
  -l=<limit>   Maximum results [default: -1]
  -o=<output>  Output file [default: scrape.json]
"""
from docopt import docopt
from tqdm import tqdm
from snscrape.modules import twitter

if __name__ == "__main__":
	args = arguments = docopt(cli, version='0.1')
	for key in ("-r","-l"):
		args[key] = int(args[key])
	scraper = twitter.TwitterSearchScraper(args["-q"],top=args["-m"]!="live",retries=args["-r"])
	with open(args["-o"],"w") as f:
		for i,tweet in tqdm(enumerate(scraper.get_items()),total=args["-l"]):
			if args["-l"]!=-1 and i>args["-l"]:
				break
			f.write(tweet.json())
			f.write("\n")
