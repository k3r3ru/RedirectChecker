import requests
import argparse

parser = argparse.ArgumentParser(prog='RedirectChecker', description='Checks a list of URLs for redirects, substituting them to the original URLs and removing any duplicates')
parser.add_argument('filepath')
args = parser.parse_args()
path = args.filepath


outUrls = []

def redirCheck(url):
    try:
        r = requests.get(url, allow_redirects=False, timeout=5)
    except:
        print(f'Connection error on {url} - Skipping...' )
        return
    
    redir = r.headers.get('location')
    if redir is not None and url != redir:
        print(f'{url} --> {redir}')
        outUrls.append(redir) if redir[-1] != '/' else outUrls.append(redir[0:-1])
    else:
        outUrls.append(url) if url[-1] != '/' else outUrls.append(url[0:-1])


try:
    with open(path) as f:
        for l in f:
            l = l.strip('\n')
            redirCheck(l)
    f.close()
except:
    print('File read error. Please check the provided path.')


outUrls = list(dict.fromkeys(outUrls))

try:
    out = open('out.txt', 'x')
    for url in outUrls:
        out.write(url+'\n')
    out.close()
except:
    print('Can\'t open output file for writing.')
