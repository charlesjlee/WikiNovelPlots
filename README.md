# WikiNovelPlots
The **WikiNovelPlots** corpus is a collection of 84,112 novel plots extracted from English language Wikipedia. These plots were extracted by looking at all English language articles under the [Novels](https://en.wikipedia.org/wiki/Category:Novels) category and its sub-categories, then grabbing the first section whose title contains the words "plot", "summary", or "synopsis".

This repository contains the corpus as a Python pickle, as well as code and instructions for how to recreate the **WikiNovelPlots** corpus.

## Use the corpus
The corpus is saved as a Python pickle to reduce disk space and stay under [GitHub's 100MB file size limit](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), and avoid the thorny problem of delimiting records with newlines and quotes. You will need Python and the `pandas` library to read the file:

```python
# extracted from view_clean_summaries.py
import pandas as pd
df = pd.read_pickle('summaries_clean.pkl', compression='xz')
df.head(5)
                        title  pageid                                      summary_clean  summary_length
0                 Animal_Farm     620  The poorly-run Manor Farm near Willingdon, Eng...            5514
1           A_Modest_Proposal     665  Swift's essay is widely held to be one of the ...            2963
2         Alexander_the_Great     783     The Killing of Cleitus, by André Castaigne ...            5650
3  A_Clockwork_Orange_(novel)     843  Part 1: Alex's world[edit]\nAlex is a 15-year-...            6705
4             Agatha_Christie     984  Christie has been called the "Duchess of Death...           10427
```

## Recreate the corpus
1. Use [this preset PetScan query](https://petscan.wmflabs.org/?psid=21520280), or navigate to the [main PetScan site](https://petscan.wmflabs.org/) and set `Categories=Novels` and `Depth=9000`
    1. Click `Do it!` to execute your query
    1. Click on `Output` and export the data as CSV
1. Execute `download_summaries.py` and pass the name of the PetScan file you just exported. This will grab the summary for each page (if availabile) and save a Python pickle named `summaries.pkl`. The script executes ~600k serial requests against the MediaWiki API and took me 22 hours to run. While one could speed this up via batch requests and parallelization, serial requests are specifically called out as following [API etiquette](https://www.mediawiki.org/wiki/API:Etiquette) and I had the time to spare.
    ```
    python download_summaries.py name_of_petscan_export.csv
    ```
1. Execute `clean_summaries.py`. This will load `summaries.pkl`, strip the HTML from and sanitize each summary, then save a Python pickle named `summaries_clean.pkl`
    ```
    python clean_summaries.py
    ```

input|step|output|output_records|output_size
--|--|--|--|--
-| export [PetScan](https://petscan.wmflabs.org/) with `Categories=Novels` and `Depth=9000`|`petscan_psid_21520280_20220223.csv`|306841|20.7 MB
`petscan_psid_21520280_20220223.csv`|`download_summaries.py`|`summaries.pkl`|306841|77.8 MB
`summaries.pkl`|`clean_summaries.py`|`summaries_clean.pkl`|84112|58 MB

## Background
This repository and dataset is my adaptation of Mark Riedl's [WikiPlots](https://github.com/markriedl/WikiPlots) repository. Mark created his version back in 2017 by taking an English Wikipedia dump, expanding it with [Wikiextractor](https://github.com/attardi/wikiextractor), and then scanning through each page. This process is labor intensive and no longer works in 2022 because of [a bug in Wikiextractor](https://github.com/attardi/wikiextractor/issues/247). I explored [a bunch of options](https://stackoverflow.com/questions/71175922/extract-story-plots-from-wikipedia) and settled on the solution in this repo that uses [PetScan](https://petscan.wmflabs.org/) and the [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page).

## Known issues
The cleaned summaries sometimes require further cleaning:
1. leftover citations, escaped characters, multiple new lines
    ```
    \n\n\n^ Berlin 2018, p.\xa01163.
    ```
1. formatting code
    ```
    .mw-parser-output .hatnote{font-style:italic}.mw-parser-output div.hatnote{padding-left:1.6em;margin-bottom:0.5em}.mw-parser-output .hatnote i{font-style:normal}.mw-parser-output .hatnote+link+.hatnote{margin-top:-0.5em}
    ```
1. cite errors
    ```
    Cite error: The named reference Genre was invoked but never defined (see the help page).
    ```
