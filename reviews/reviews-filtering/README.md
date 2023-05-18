## Filtering

The **feature-list.csv** file contains the different gamification features, along with the synonyms and stems that are used as search criteria for that feature.
The reviews are then filtered to identify which reviews mention which feature.

For each feature, the reviews that mention it are tallied according to sentiment (in the _positiveCount_ and _negativeCount_ columns), viewable in the **feature-scores.csv** file.
An average 'sentiment score' for each feature is also calculated, where review with negative sentiment has a score of -1, and a review of positive sentiment has a score of 1, added up and divided by the total number of reviews.

This is also done with individual apps, to look at the reviews mentioning a feature from that specific app. This is in the **feature-scores-by-app.csv** file.

The filtering for features is also done with a smaller subset of reviews that specifically mention python. This is in the **feature-scores_python.csv** and **feature-scores-by-app_python.csv** files.

The overall sentiment by app is also calculated, where all the reviews of an app are tallied according to sentiment, disregarding which gamification feature the reviews mention, or even if a feature is mentioned at all. This is in the **app-scores.csv** file.

## Reviews

The reviews themselves are stored in the different subdirectories. These only contain the review data that was used in the filtering. 

- **review-files-combined** contains all the raw review data of each app, combining the google play and app store reviews for each app.
- **review-files-combined-standardized** contains the review data of each app, where the review content has been standardized (lowercased, punctuation, stop words, excess whitespace,  non-ascii characters removed)
- **review-files-combined-filtered** has the previously standardized reviews filtered by the gamification features. The _mentionedSynonym_ column contains a list the game features' synonyms and their stems that was found in the review. The _mentionedFeature_ column contains the actual list of features that those matched strings correspond to.
- The standardized and filtered reviews mentioning python are in equivalent files and folders named **...-python...**


Example  

A review for sololearn is: "...you aren't reducing the wait time, but hopefully I will get used to it..."  
The standardized review is: "...arent reducing wait time hopefully get used..."  
This review contains the phrase "wait time" , which is a synonym for the gamification feature "torture breaks".  
This review is then considered to be talking about torture breaks. It has a positive sentiment, so it counts as a positive review for torture breaks.


