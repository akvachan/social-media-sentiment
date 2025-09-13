# social-media-sentiment

Example of social media sentiment data preprocessing and analysis workflow.

# Data 
The dataset consists of more than 14,000 tweets directed at six major U.S. airlines—American Airlines, JetBlue, Southwest, United, US Airways, and Virgin America—collected over nine consecutive days in February 2015. Each tweet includes its text, timestamp, and associated sentiment label (positive, neutral, or negative) assigned by a machine learning model, along with a confidence score. The datasets can be merged using a common identifier and allow for analysis of airline-specific mentions, customer sentiment trends, and overall public perception of airlines on Twitter during the period.

# Preprocessing
`main.py` does following data preprocessing:
- Loads data in csv format
- Removes duplicates in the data
- Removes null values in the data
- Merges two tables on the common identifier 
- Creates a new column 'mention' based on the old column 'text'

# Running 
```sh
uv run main.py
```
