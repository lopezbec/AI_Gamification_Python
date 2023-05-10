# Machine Learning and Gamification for a personalized-adaptive educational application 
**[Inteligencia Artificial y Gamificación Personalizada-Adaptativa para la Formación en Programación]**
[Website of the project](https://sites.lafayette.edu/lopezbec/projects/machine-learning-and-gamification-for-a-personalized-adaptive-educational-application/)
## Abstract

This project is supported by the National Fund for Innovation and Scientific and Technological Development (FONDOCyT for its acronym in Spanish) from the Ministry of Higher Education, Science, and Technology of the Dominican Republic (**FONDOCYT 2022-3A1-112**), and is in collaboration with the Universidad Nacional Pedro Henríquez Ureña (UNPHU) and the  Asociación para la Creatividad, Innovación, Emprendimiento y Networking (A100%) from the Dominican Republic.

The project aims to explore the implementation of Machine Learning algorithms in a gamified educational application to personalize its game elements and adapt its pedagogical content.  The application will focus on helping its users learn to program using Python since Python Software Developers are among the most in-demand emerging professions. The application will implement Machine Learning algorithms to offer optimal scaffolding learning to students. This is by implementing interactive and individualized content capable of adapting to the level of knowledge and learning pace of the users. Nevertheless, the positive effects of an intelligent learning system on the learning of its users depend directly on their level of engagement and motivation. An effective method to increase user engagement and motivation in learning applications is by using gamification. Unfortunately, gamifying an application does not ensure that it will motivate all its users since the preference for game elements differs significantly between individuals. Therefore, to maximize the motivation of the users, this proposal seeks to leverage Recommendation Systems to personalize its game elements.

___________________________________________________

#  Code, Algorithms, and Models implementation
___________________________________________________

## Google Play and Apple Store App Reviews Scraping

<table align="left">
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/lopezbec/AI_Gamification_Python/blob/main/reviews/appreviews.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Apps Reviews Scrapping</a>
  </td>
</table>
<br><br></br>

This project allows you to gather reviews from any app that is found on Google Play or AppStore. It lets you choose multiple options, from gathering specific number of reviews, to specify the rating of desire from the app.
The google collab grants you via forms, a visual cue of how the reviews are gathered and are saved specifically.

## Sentiment and NER analysis on reviews

<table align="left">
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/lopezbec/AI_Gamification_Python/blob/main/reviews/appreviews_sentiment.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Apps Reviews Sentiment</a>
  </td>
</table>
<br><br></br>

This notebook allows you to get the sentiment (positive, negative or neutral) of the reviews that were scraped stored on the repo, in both Spanish or English. The interactive colab forms provides visual indicators of what reviews are analyzed. 

<table align="left">
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/lopezbec/AI_Gamification_Python/blob/main/reviews/appreviews_NER.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Apps Reviews NER</a>
  </td>
</table>
<br><br></br>

This notebook allows you to perform NER (Name Entity Recognition) analysis on the reviews that were scraped stored on the repo. The interactive colab forms provides visual indicators of what reviews are analyzed. 
___________________________________________________

#  Prototype of Application   
___________________________________________________
## Example of Application Hexad Player type and User Data Interface
This is a example of the "intro page" for the app and study itself (v 3_26_23)

[Screencast from 04-07-2023 11:55:59 AM.webm](https://user-images.githubusercontent.com/106645242/230639504-9ef200a2-7bbb-4cf5-857b-179b8565507a.webm)


## Example of Application Pedagogical/Question Interfaces

This is an example

https://user-images.githubusercontent.com/113645268/235823495-16584a65-31c8-4393-a44e-f1384669f4ea.mp4

___________________________________________________

#  Data and more
___________________________________________________

The team has collected online reviews from users of similar educational gamified applications in Google Play and Apple App Store (using the (Google Play and Apple Store App Reviews Scrapping notebook above). This with the objective to gain a better understanding of what makes some apps “better” than other. Some summary statistics of the reviews are shown below.


|    | Name                   |   ReviewCount |   AverageRating |   AverageReviewLength | EarliestDate        | LatestDate          |   AppleStoreReviews |   GooglePlayReviews |
|---:|:-----------------------|--------------:|----------------:|----------------------:|:--------------------|:--------------------|--------------------:|--------------------:|
|  0 | codeacademy            |          3573 |         3.75679 |               88.5665 | 2018-08-01 01:33:12 | 2023-03-24 22:07:12 |                 473 |                3100 |
|  1 | datacamp               |          7719 |         4.47882 |               76.3687 | 2017-10-18 11:23:14 | 2023-03-24 21:09:12 |                 341 |                7378 |
|  2 | encode                 |          2045 |         4.63081 |               91.7667 | 2016-03-13 23:11:32 | 2023-03-19 01:47:34 |                 184 |                1861 |
|  3 | learn-python-programiz |          4814 |         4.65351 |               60.8224 | 2019-08-22 19:39:09 | 2023-03-25 13:34:31 |                  86 |                4728 |
|  4 | mimo                   |         88724 |         4.53408 |               63.3281 | 2016-08-19 21:15:07 | 2023-03-25 15:45:02 |                2000 |               86724 |
|  5 | programming-hero       |         16538 |         4.78069 |               57.101  | 2018-11-28 09:32:14 | 2023-03-25 14:57:48 |                 131 |               16407 |
|  6 | programming-hub        |         49549 |         4.58268 |               60.9303 | 2013-07-31 05:45:19 | 2023-03-25 14:57:25 |                 867 |               48682 |
|  7 | sololearn              |        132553 |         4.71747 |               61.8852 | 2016-10-26 02:56:32 | 2023-03-25 16:36:13 |                1702 |              130851 |



