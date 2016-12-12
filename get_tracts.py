#!/usr/bin/env python
from __future__ import print_function

import posixpath

import requests
from lxml.etree import HTML

BASE_URL = 'http://www2.census.gov/geo/tiger/TIGER2012/TRACT/'

def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


def main():
    r = requests.get(BASE_URL)

    for filename in HTML(r.content).xpath('//a[starts-with(@href, "tl_2012_")]/@href'):
        print("Downloading", filename)
        download_file(posixpath.join(BASE_URL, filename))


if __name__ == '__main__':
    main()
