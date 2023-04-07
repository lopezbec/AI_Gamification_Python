import pandas as pd
import flair
import os
from flair.data import Sentence
from flair.models import SequenceTagger
import sys 
from tqdm import tqdm
if len(sys.argv) < 2:
    print('Please provide input file name as command line argument')
    sys.exit(1)

# Get the input file name from command line argument
input_file = sys.argv[1]

# load tagger
tagger = SequenceTagger.load("flair/ner-english-large")
#load the Flair NER tag

# load the CSV file
df = pd.read_csv(input_file)

# create an empty dataframe to store the NER output
output_df = pd.DataFrame(columns=['reviewId', 'NER_Text', 'Start_Pos', 'Eng_Pos', 'NER_Label', 'Prob'])

# iterate over each row of the input dataframe
for index, row in tqdm( df.iterrows()):
    # get the content and content_ID from the current row
    content = row['review']
    content_id = row[0]
    try: 
    # create a Flair sentence from the content
        sentence = Sentence(content)
   # print(sentence)
    # run NER on the sentence
        tagger.predict(sentence)
    except:
        continue
    
    # iterate over each entity in the sentence and add it to the output dataframe
    for entity in sentence.get_spans('ner'):
        
        output_df = output_df.append({
            'reviewId': content_id,
            'NER_Text': entity.text,
            'Start_Pos': entity.start_pos,
            'End_Pos': entity.end_pos,
            'NER_Label': entity.tag,
            'Prob': entity.score
        }, ignore_index=True)

# save the output dataframe to a CSV file
output_file = os.path.splitext(input_file)[0] + "_NER.csv"
output_df.to_csv(output_file, index=False)

