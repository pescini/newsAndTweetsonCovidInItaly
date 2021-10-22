cli="""
Usage:
  jsonlist2csv.py ( (-h | --help) | --version )
  jsonlist2csv.py [-i=FILE] [-o=FILE]

Options:
  -h --help  Show this screen.
  --version  Show version info.
  -i=FILE    Input file [default: scraped.json]
  -o=FILE    Output file [default: scraped.csv]
"""
from docopt import docopt
from tqdm import tqdm
import json, os
from datetime import date, timedelta

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if __name__ == "__main__":
	args = arguments = docopt(cli, version='0.1')
	NoneList = lambda x: x if x!=None else []
	with open(args["-i"]) as inf, open(args["-o"],"wb") as ouf:
		ouf.write("user; datetime; text; source; retweet; like; reply; quote; hashtags; mentions\n".encode('utf8'))
		for line in tqdm(inf,total=file_len(args["-i"])):
			if line.strip()!="":
				d = json.loads(line)
				ouf.write(";".join([
					d["user"]["username"],d["date"][:19],'"%s"' % d["content"].replace("\n"," ").replace('"','""'),d["sourceLabel"],
					str(d["retweetCount"]),str(d["likeCount"]),str(d["replyCount"]),str(d["quoteCount"]),
					",".join(NoneList(d["hashtags"])),",".join(x["username"] for x in NoneList(d["mentionedUsers"]))
				+ "\n"]).encode('utf8'))