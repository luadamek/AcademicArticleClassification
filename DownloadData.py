#!/usr/bin/env python
# coding: utf-8

# In[7]:


#scour the web for arxiv articles

classes = ["Mathematics", "Computer Science", "Quantitative Biology",           "Quantitative Finance", "Statistics",           "Electrical Engineering and Systems Science", "Economics","Physics"]

# a map of all the document codes for things uploaded into arxix
subclass_map = {
    "Physics":["astro-ph","cond-mat","gr-qc","hep-ex","hep-lat",\
              "hep-ph","hep-th","math-ph","nlin","nucl-ex","nucl-th"\
              "physics","quant-ph"],\
    "Mathematics":["math"],\
    "Computer Science":["CoRR"],\
    "Quantitative Biology":["q-bio"],\
    "Quantitative Finance":["q-fin"],\
    "Statistics":["stat"],\
    "Electrical Engineering and Systems Science":["eess"],\
    "Economics":["econ"],\
}

class_indices = {c:i for i, c in enumerate(classes)}

for c in classes:
    print(c)
    assert c in subclass_map
for c in subclass_map:
    assert c in classes

import datetime
now = datetime.datetime.now()
print(now.year, now.month, now.day, now.hour, now.minute, now.second)

times = []
for year in range(now.year, now.year-2, -1): #download articles for this year and last year
    if now.year == year:
        max_month = now.month
    else:
        max_month = 12
    for month in range(1, max_month + 1):
        times.append("{:02d}{:02d}".format(year - 2000, month))


# In[ ]:


from urllib.request import urlopen
basedir = "https://export.arxiv.org/"
import requests
import os
from bs4 import BeautifulSoup

def download_file(path, destination):
    r = requests.get(path, stream=True)
    downloads_dir = "downloaded_files"
    if not os.path.exists(destination):
        os.makedirs(destination)
    fname = os.path.join(destination, path.split("/")[-1])
    if os.path.exists(fname): return
    with open(fname, "wb") as fd:
        for chunk in r.iter_content(200000):
            fd.write(chunk)


def get_soup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    return soup


for c in classes:
    subclasses = subclass_map[c]
    for subclass in subclasses:
        for time in times:
            url = basedir + "list/{}/{}?show=2000".format(subclass, time)
            print(url)
            soup = get_soup(url)

            print("Downloading Abstracts")
            this_path = os.path.join("abstracts", c, subclass, time)
            for i, link in enumerate(soup.find_all("a")):
                try:
                    href = link.get('href')
                    if not href: continue
                    if "/abs/" not in href: continue
                    if "https:" in href: continue
                    this_url = basedir + href
                    fname = os.path.join(this_path, this_url.split("/")[-1] + ".txt")
                    print(this_url)
                    if os.path.exists(fname): continue
                    this_soup = get_soup(this_url)
                    text = this_soup.get_text()
                    abstract_string = "Abstract:"
                    index = text.find(abstract_string)
                    text = text[index + len(abstract_string):]
                    end_of_abstract_string = "\n\n\n"
                    index = text.find(end_of_abstract_string)
                    text = text[:index] #this is the abstract
                    #write the abstract to an output fil
                    if not os.path.exists(this_path): os.makedirs(this_path)
                    with open(fname, "w") as f:
                        f.write(text)
                except Exception as e: pass

            print("Downloading PDFS")
            this_path = os.path.join("datasets", c, subclass, time)
            count = 0
            for link in soup.find_all('a'):
                try:
                    href = link.get('href')
                    if not href: continue
                    if "https:" in href: continue
                    if count == 5: break
                    if "/pdf/" not in href: continue
                    this_url = basedir + href  + ".pdf"
                    print(this_url)
                    download_file(this_url, this_path)
                    count += 1
                except Exception as e: pass




