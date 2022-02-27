import pandas as pd

pd.options.display.max_columns = None

if __name__ == "__main__":
    df = pd.read_pickle('summaries_clean.pkl', compression='xz')
    print(df.head(5))
