# social-media-sentiment

Example of social media sentiment data preprocessing and analysis workflow.

`main.py` does following data preprocessing:
- Loads data in csv format
- Removes duplicates in the data
- Removes null values in the data
- Merges two tables on the key column
- Creates a new column 'mention' based on the old column 'text'

# Running 
```sh
uv run main.py
```
