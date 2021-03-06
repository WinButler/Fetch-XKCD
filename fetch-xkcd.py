import urllib, urllib2, re, sys, os, time
from HTMLParser import HTMLParser
# Defining our method of removing HTML tags from alt text when naming retrieved
# files.
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
# Function that will strip HTML tags from a string.
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
# Main function.
def main(argv):
    def usage():
        print("""ABOUT//

Fetch-XKCD v1.0!

Fetch-XKCD is a tool for downloading and updating a collection of comics from popular webcomic xkcd.com. Simply put it in an empty directory and run it to fill that directory with every comic. Then whenever you want to update your collection, simply run it again.

Fetch-XKCD was written in Python 2.7.3 and may not work in Python 3.x.

USAGE//

Place fetch-xkcd.py into an empty directory and run it. To bring your collection up to date, run it again.

optional arguments:
  -h, --help              show this help message and exit""")
    for arg in argv:
        if 'h' in arg:
            usage()
            sys.exit()
    print('\n')
    print('  _____    _       _         __  ___  ______ ____  ')
    print(' |  ___|__| |_ ___| |__      \ \/ / |/ / ___|  _ \ ')
    print(" | |_ / _ \ __/ __| '_ \ _____\  /| ' / |   | | | |")
    print(' |  _|  __/ || (__| | | |_____/  \| . \ |___| |_| |')
    print(' |_|  \___|\__\___|_| |_|    /_/\_\_|\_\____|____/ ')
    print('                                                   ')
    print('\n* Fetch-XKCD v1.0\n\n')
    print('* Check out the latest merch at store.xkcd.com - support your favorite comic!\n')
    time.sleep(1)
    print('* Check out the latest merch at store.xkcd.com - support your favorite comic!\n')
    time.sleep(1)
    print('* Check out the latest merch at store.xkcd.com - support your favorite comic!\n')
    time.sleep(1)
    print('* Check out the latest merch at store.xkcd.com - support your favorite comic!\n')
    time.sleep(1)
    print('* Check out the latest merch at store.xkcd.com - support your favorite comic!\n')
    time.sleep(1)
    print('* Checking xkcd.com for total comics in database...')
    xkcdhomestring = urllib2.urlopen('http://xkcd.com/').read()
    # Get number of comics available so we know how many to retrieve.
    totalzoom1 = re.search('<a rel="prev".+?>', xkcdhomestring).group(0)
    total = int(re.search('\d+', totalzoom1).group(0)) + 1
    print('* ' + str(total) + ' comics found in database.\n')
    total_fetched = 0
    # Create a list of all comics already downloaded.
    print('* Checking for gaps in your comic collection...')
    filelist = os.listdir('.')
    removethese = []
    for i in filelist:
        if i[-3:] not in ['jpg', 'png', 'gif']:
            removethese.append(i)
    for i in removethese:
        filelist.remove(i)
    comicnumbers = []
    for i in filelist:
        comicnumbers.append(int(re.search('\d+ -', i).group(0)[:-2]))
    # Loop through all the comics, retrieve and rename every one in local
    # working directory.
    print('* Done evaluating collection.\n')
    print('* Retrieving all comics not already in your collection...\n')
    for i in range(total):
        if str(i+1) == '404':
            continue
        if (i+1) not in comicnumbers:
            print('* Fetching comic #' + str(i+1) + '...')
            xkcd = urllib2.urlopen('http://xkcd.com/' + str(i+1) + '/')
            img = re.search('<img src="http://imgs.xkcd.com/comics/.*?/>', xkcd.read(), re.DOTALL).group(0)
            imgurl = re.search('http://imgs.xkcd.com/comics/.*?(\.jpg|\.png|\.gif)', img).group(0)
            if imgurl[-3:] == 'jpg':
                ext = '.jpg'
            elif imgurl[-3:] == 'png':
                ext = '.png'
            elif imgurl[-3:] == 'gif':
                ext = '.gif'
            alt = re.search('alt=".+?"', img).group(0)[5:-1]
            # To make sure our filename is writable, we strip HTML tags, and
            # strip any character not in the whitelist.
            valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 -_()!@#$%^&+=;'\",.~`"
            parser = HTMLParser()
            valid_filename = strip_tags(str(parser.unescape(''.join(c for c in alt if c in valid_chars))))
            target_filename = str(i+1) + ' - ' + valid_filename + ext
            urllib.urlretrieve(imgurl, target_filename)
            total_fetched += 1
            print("* Success! Comic saved as: \"" + target_filename + "\"")
    print('\n* Total files retrieved: ' + str(total_fetched) + '\n')
    print("* Fetch-XKCD finished! Enjoy your comics!")
    time.sleep(10)
if __name__ == '__main__':
    main(sys.argv[1:])
