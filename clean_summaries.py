import pandas as pd
import pywikibot
import re
from tqdm import tqdm

tqdm.pandas()
pd.options.display.max_columns = None

def clean_summary(summary):
    stripped_summary = pywikibot.textlib.removeHTMLParts(summary, keeptags=[])
    
    # remove the edit tag and its text, e.g. Plot introduction[edit]\n
    if '[edit]\n' in stripped_summary:
        stripped_summary = stripped_summary[stripped_summary.index('[edit]\n') + len('[edit]\n'):]
        
    # remove citatations, e.g. [1]
    stripped_summary = re.sub(r'\[\d*\]', '', stripped_summary)

    # remove trailing whitespace
    stripped_summary = stripped_summary.rstrip()
    
    return stripped_summary

if __name__ == "__main__":
    df = pd.read_pickle('summaries.pkl', compression='xz')

    df['summary_clean'] = df.summary.progress_apply(clean_summary)
    df['summary_length'] = df.summary_clean.progress_apply(len)
    
    df = df[['title', 'pageid', 'summary_clean', 'summary_length']]
    df = df[df.summary_length > 0]
    df.reset_index(drop=True, inplace=True)
    
    df.to_pickle('summaries_clean.pkl', compression='xz')
