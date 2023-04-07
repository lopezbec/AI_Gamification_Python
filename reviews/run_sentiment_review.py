import os
import sys
import pandas as pd
from flair.models import TextClassifier
from flair.data import Sentence
from tqdm import tqdm

if len(sys.argv) < 2:
    print('Please provide input file name as command line argument')
    sys.exit(1)

# Get the input file name from command line argument
input_file = sys.argv[1]

# Load the CSV file into a dataframe
df = pd.read_csv(input_file)

# Initialize Flair Sentiment Classifier
classifier = TextClassifier.load('en-sentiment')
if input_file.endswith(".csv"):
# Loop over each row in the dataframe and predict sentiment for the review content
    sentiments = []
    if input_file.startswith("applestore"):
        for content in tqdm(df['review']):
            try:
                sentence = Sentence(content)
                classifier.predict(sentence)
                sentiment = sentence.labels[0].value
                sentiments.append(sentiment)
                df['sentiment']=sentiments
            except:
                continue

    else:
        for content in tqdm(df['content']):
            try:
                sentence = Sentence(content)
                classifier.predict(sentence)
                sentiment = sentence.labels[0].value
                sentiments.append(sentiment)
                df['sentiment']=sentiments
            except:
                continue

        
# Add the sentiment column to the dataframe
   # df['sentiment'] = sentiments

# Get the output file name by appending "_sentiment" before the file extension
    output_file = os.path.splitext(input_file)[0] + "_sentiment.csv"

# Save the new CSV file with sentiment column
    df.to_csv(output_file, index=False)

    print('Sentiment analysis completed and saved to:', output_file)

