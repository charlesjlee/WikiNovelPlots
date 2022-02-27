import pandas as pd
import requests
import sys
from tenacity import retry, wait_exponential, stop_after_attempt
from tqdm import tqdm

tqdm.pandas()
pd.options.display.max_columns = None

def looks_like_plot(s):
    # effective for novels according to https://github.com/markriedl/WikiPlots/issues/1
    return any(x in s.lower() for x in ('plot', 'summary', 'synopsis'))

@retry(wait=wait_exponential(multiplier=1, min=1, max=60), stop=stop_after_attempt(10))
def get_plot_from_pageid(row):
    api_route_prefix = f'https://en.wikipedia.org/w/api.php?action=parse&pageid={row.pageid}&format=json&maxlag=5'
    request = requests.get(f'{api_route_prefix}&prop=sections').json()
    
    if 'error' in request:
        if request['error']['code'] == 'nosuchpageid':
            return ''
    
    # find first `line` that looks like a plot
    for section in request['parse']['sections']:
        if looks_like_plot(section['line']):            
            # get that section's text
            data = requests.get(f"{api_route_prefix}&prop=text&section={section['index']}").json()
            return data['parse']['text']['*']
    
    return ''
            
if __name__ == "__main__":
    petscan_file_name = sys.argv[1] if len(sys.argv) == 2 else 'petscan_psid_21520280_20220223.csv'
    
    df = pd.read_csv(petscan_file_name, escapechar='\\')
    df = df[['title', 'pageid']]
        
    df['summary'] = df.progress_apply(get_plot_from_pageid, axis=1)    
    df.to_pickle('summaries.pkl', compression='xz')
