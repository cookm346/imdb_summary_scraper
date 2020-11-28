import requests
from bs4 import BeautifulSoup as bs
import numpy as np

def get_string(p):
  s = ""
  for part in p.contents:
    s += part.string
  return s

def get_summaries(url):
  r = requests.get(url)
  soup = bs(r.content, "html.parser")
  ps = soup.find_all("p", class_="text-muted")
  ps = ps[1: :2]
  r = []
  for p in ps:
    r.append(get_string(p))
  return r

def get_next_url(base_url, start):
  return base_url + "&start=" + str(start)

def get_all_summaries(url, n_pages):
  links = []
  start = 1
  for _ in range(0, n_pages):
    links.append(get_summaries(url))
    start += 50
    url = get_next_url(url, start)
  return np.array(links).flatten()

def write_summaries(summaries, dir):
  for i, summary in enumerate(summaries):
    text_file = open(dir + "/" + str(i) + ".txt", "w")
    text_file.write(summary)
    text_file.close()

n_pages = 14

sci_fi_summaries = get_all_summaries("https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=sci-fi&sort=user_rating,desc&ref_=adv_prv", n_pages)

write_summaries(sci_fi_summaries, "sci-fi")


romance_summaries = get_all_summaries("https://www.imdb.com/search/title/?genres=romance&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=AJ3Y950PT2HFV2ZMVT08&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_16", n_pages)

write_summaries(romance_summaries, "romance")
