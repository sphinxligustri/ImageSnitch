
from serpapi import GoogleSearch
import requests
import argparse
import os
from pathlib import Path

# if dir exist: notify, then exit 
# elif link is not image: notify, then exit 
# else: create dir
#   download image to dir
#   fetch exact matches links, and make html, and store in dir

def append_gallery(fname, payload):
  with open(fname, 'a+') as f:
    f.write(payload)

def is_url_image(url):
  result = False
  image_formats = ("image/png", "image/jpeg", "image/jpg", "image/webp")
  try:
    r = requests.head(url)
    if r.headers["content-type"] in image_formats:
        result = True
  except:
    pass
  return result

def save_image(image, img_data):
  with open(image, 'wb+') as f:
    f.write(img_data)

def search_params(url, match_type, api_key):
  return {
    "engine": "google_lens",
    "type": match_type,
    "url": url,
    "api_key": api_key
  }

def matches_for(match_type, params):
  search = GoogleSearch(params)
  results = search.get_dict()
  if "exact_matches" in results.keys():
    return results["exact_matches"]
  else:
    print(f'No matches for {match_type=}')
    return []

def links_from(matches):
  result = ''
  for match in matches:
    result += f'<a href="{match["link"]}">{match["link"]}</a><br>\n'
  return result

def parse_cli_arguments():
    parser = argparse.ArgumentParser(
        prog='ImageSnitch',
        description='Tell me where Google has found this exact image.')
    parser.add_argument('-s', '--sourcelink', help="Image source URL for query.")
    parser.add_argument('-d', '--targetdir', help="Where to store results. Defaults to CWD.") 
    parser.add_argument('-k', '--apikey', help="API key to authorize to use SerpApi.") 
    args = parser.parse_args()
    return args    


if __name__ == '__main__':
    args = parse_cli_arguments()

    cwd = os.getcwd()
    api_key = args.apikey
    url = args.sourcelink
    target_dir = args.targetdir if args.targetdir else cwd
    # rewrite url to valid file/dir name
    target_dir = f'{target_dir}/{url.replace('/', '+')}'

    # if dir exist: notify, then exit 
    # elif link is not image: notify, then exit 
    # else: create dir
    #   download image to dir
    #   fetch exact matches links, and make html, and store in dir
    if os.path.isdir(target_dir) or os.path.isfile(target_dir):
        print('Directory already exists. Delete or move it to re-do action.')
        exit()
    elif not is_url_image(url):
        print('No image found at provided URL.')
        exit()

    file = f'./{url.split('/')[-1]}'
    image_file = f'{target_dir}/{file}'
    gallery_file = f'{target_dir}/links.html'
    print(f'Processing {url=}')
    Path(target_dir).mkdir(parents=True)

    try:
        img_data = requests.get(url).content
        save_image(image_file, img_data)
        append_gallery(gallery_file, f'<a href="{url}"> <img src="{url}" loading="lazy" /></a><br>\n')
    except:
        print('An error occurred during image request.')
        exit()
    
    params = search_params(url=url, match_type='exact_matches', api_key=api_key)
    matches = matches_for('exact_matches', params=params)
    append_gallery(gallery_file, payload=links_from(matches))