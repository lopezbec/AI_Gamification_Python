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

This notebook allows you to get the sentiment (positive, negative, or neutral) of the reviews that were scraped and stored on the repo, in both Spanish and English. The interactive colab forms provide visual indicators of what reviews are analyzed. 

<table align="left">
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/lopezbec/AI_Gamification_Python/blob/main/reviews/appreviews_NER.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Apps Reviews NER</a>
  </td>
</table>
<br><br></br>

This notebook allows you to perform NER (Name Entity Recognition) analysis on the reviews that were scraped and stored on the repo. The interactive colab forms provide visual indicators of what reviews are analyzed. 

## Bigram Networks of Reviews

<table align="left">
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/lopezbec/AI_Gamification_Python/blob/main/reviews/bigram-network/bigram_networks_interactive.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Bigram Networks</a>
  </td>
</table>
<br><br></br>

This notebook allows you to plot the bigram networks of reviews per app and overall, either with the entire review text or the NER tags. There are visual indicators of the frequency of the bigrams (as the width of the edges) and the average sentiment of the reviews the bigrams appear in (as the color of the edges).
___________________________________________________

#  Prototype of Application   
___________________________________________________
## Example of Application Hexad Player type and User Data Interface
This is an example of the "intro page" for the app and study itself (v 3_26_23)

[Screencast from 04-07-2023 11:55:59 AM.webm](https://user-images.githubusercontent.com/106645242/230639504-9ef200a2-7bbb-4cf5-857b-179b8565507a.webm)


## Examples of Application Pedagogical/Question all in one Interface / Lesson 1 and 2

Lesson 1 Complete

[Video_Pedagogical_Question_Lesson1_Complete.webm](https://github.com/lopezbec/AI_Gamification_Python/assets/113645268/15d74d61-ac00-4658-acf8-ba36603a274c)

Lesson 2 Complete

[Video_Pedagogical_Question_Lesson2_Complete.webm](https://github.com/lopezbec/AI_Gamification_Python/assets/113645268/384deacf-48e8-4e04-a95a-b32045ad548c)

___________________________________________________

#  How to run the prototype of the application:
___________________________________________________

1- Install Anaconda distribution (If you have Anaconda already, skip this step):

- Go to this link and follow the instructions: [https://www.anaconda.com/download](https://www.anaconda.com/download)
- 
  (If you have issues installing the latest version of Anaconda, you can download a previous/older version here:  [https://repo.anaconda.com/archive/](https://repo.anaconda.com/archive/))

 2- Download the repo:
 
 - Go to the "<> Code" button on the top right corner of this screen (you will need to scroll up)
 - Click the "Download Zip" option (this will download the whole repo to your computer)
 - Find the location where the file was downloaded, and decompress the file (like right-click and "extract all" if in Windows)
 - Copy and paste the directory path of this folder (see video how-to for [Windows](https://www.youtube.com/watch?v=QZUpzuQ0X5I) or [Mac](https://www.youtube.com/watch?v=kIhGavBqXYc) 

 3- Install Anaconda enviroment:
 
 - Open the Anaconda prompt (in a Mac open the Terminal)
 - Once it is open you will type "cd" and subsequently paste the directory path of the repo you downloaded and decompressed in the previous part (it should be something like ".../AI_Gamification_Python") and press ENTER
 - Create a new conda environment with python by typing "conda create --name test python" and press ENTER
 - Type "conda activate test" and press ENTER
 - Install PyQT6 in the environment by typing "pip install PyQt6-tools==6.4.2" and press ENTER.
   
  4- Run the prototype:
   - Now type  "cd ./Elmer/Daniel_JSON_Files_Elmer" and press ENTER
   - Now type "Python Main_Modulos_Intro_Pages.py" and press ENTER. This will run the prototype

*After following all these steps the prototype will open. If you exit the prototype and would like to open it again you can:

 - Open the Anaconda prompt window
 - Type "conda activate test" and press ENTER
 - Type "cd" followed by the directory path of the folder you downloaded above
 - Now follows the step #4 above

## How to video for Mac OS [HERE](https://youtu.be/IxdrbJuCo0g)
___________________________________________________

#  Data and more
___________________________________________________

The team has collected online reviews from users of similar educational gamified applications in Google Play and Apple App Store (using the Google Play and Apple Store App Reviews Scrapping notebook above). This with the objective to gain a better understanding of what makes some apps “better” than other. Some summary statistics of the reviews are shown below.

---

**English Reviews**

*Combined Reviews*

|    | Name                   |   ReviewCount |   AverageRating |   AverageReviewLength | EarliestDate        | LatestDate          |   PositiveReviewProportion |   NeutralReviewProportion |   NegativeReviewProportion |
|---:|:-----------------------|--------------:|----------------:|----------------------:|:--------------------|:--------------------|---------------------------:|--------------------------:|---------------------------:|
|  0 | codeacademy            |          3573 |         3.75679 |               88.5665 | 2018-08-01 01:33:12 | 2023-03-24 22:07:12 |                   0.625245 |                         0 |                  0.374755  |
|  1 | datacamp               |          7719 |         4.47882 |               76.3687 | 2017-10-18 11:23:14 | 2023-03-24 21:09:12 |                   0.832621 |                         0 |                  0.167379  |
|  2 | encode                 |          2045 |         4.63081 |               91.7667 | 2016-03-13 23:11:32 | 2023-03-19 01:47:34 |                   0.866504 |                         0 |                  0.133496  |
|  3 | learn-python-programiz |          4814 |         4.65351 |               60.8224 | 2019-08-22 19:39:09 | 2023-03-25 13:34:31 |                   0.860823 |                         0 |                  0.139177  |
|  4 | mimo                   |         88724 |         4.53408 |               63.3281 | 2016-08-19 21:15:07 | 2023-03-25 15:45:02 |                   0.8589   |                         0 |                  0.1411    |
|  5 | programming-hero       |         16538 |         4.78069 |               57.101  | 2018-11-28 09:32:14 | 2023-03-25 14:57:48 |                   0.899202 |                         0 |                  0.100798  |
|  6 | programming-hub        |         49549 |         4.58268 |               60.9303 | 2013-07-31 05:45:19 | 2023-03-25 14:57:25 |                   0.855638 |                         0 |                  0.144362  |
|  7 | sololearn              |        132553 |         4.71747 |               61.8852 | 2016-10-26 02:56:32 | 2023-03-25 16:36:13 |                   0.904174 |                         0 |                  0.0958258 |


*Google Play Store Reviews*

|    | Name                   |   ReviewCount |   AverageRating |   AverageReviewLength | EarliestDate        | LatestDate          |   PositiveReviewProportion |   NeutralReviewProportion |   NegativeReviewProportion |
|---:|:-----------------------|--------------:|----------------:|----------------------:|:--------------------|:--------------------|---------------------------:|--------------------------:|---------------------------:|
|  0 | codeacademy            |          3100 |         3.84613 |               70.2368 | 2018-08-02 08:35:59 | 2023-03-24 00:51:56 |                   0.657419 |                         0 |                  0.342581  |
|  1 | datacamp               |          7378 |         4.4958  |               69.9044 | 2017-10-18 11:23:14 | 2023-03-24 21:09:12 |                   0.838439 |                         0 |                  0.161561  |
|  2 | encode                 |          1861 |         4.65395 |               77.0645 | 2016-03-13 23:11:32 | 2023-03-19 01:47:34 |                   0.875873 |                         0 |                  0.124127  |
|  3 | learn-python-programiz |          4728 |         4.65609 |               59.3101 | 2021-02-19 03:24:40 | 2023-03-25 13:34:31 |                   0.86231  |                         0 |                  0.13769   |
|  4 | mimo                   |         86724 |         4.54521 |               59.2171 | 2018-05-02 03:23:09 | 2023-03-25 15:45:02 |                   0.864075 |                         0 |                  0.135925  |
|  5 | programming-hero       |         16407 |         4.78308 |               56.6918 | 2018-11-28 09:32:14 | 2023-03-25 14:57:48 |                   0.900104 |                         0 |                  0.0998964 |
|  6 | programming-hub        |         48682 |         4.58751 |               59.5454 | 2013-07-31 05:45:19 | 2023-03-25 14:57:25 |                   0.857812 |                         0 |                  0.142188  |
|  7 | sololearn              |        130851 |         4.72481 |               59.9274 | 2016-10-26 02:56:32 | 2023-03-25 16:36:13 |                   0.907253 |                         0 |                  0.0927467 |

*Apple Store Reviews*

|    | Name                   |   ReviewCount |   AverageRating |   AverageReviewLength | EarliestDate        | LatestDate          |   PositiveReviewProportion |   NeutralReviewProportion |   NegativeReviewProportion |
|---:|:-----------------------|--------------:|----------------:|----------------------:|:--------------------|:--------------------|---------------------------:|--------------------------:|---------------------------:|
|  0 | codeacademy            |           473 |         3.17125 |               208.279 | 2018-08-01 01:33:12 | 2023-03-24 22:07:12 |                   0.414376 |                         0 |                   0.585624 |
|  1 | datacamp               |           341 |         4.11144 |               215.642 | 2017-10-19 13:14:06 | 2023-03-14 15:45:30 |                   0.706745 |                         0 |                   0.293255 |
|  2 | encode                 |           184 |         4.39674 |               239.424 | 2017-02-07 21:05:43 | 2023-02-01 20:04:49 |                   0.771739 |                         0 |                   0.228261 |
|  3 | learn-python-programiz |            86 |         4.51163 |               143.442 | 2019-08-22 19:39:09 | 2023-03-19 22:12:10 |                   0.77907  |                         0 |                   0.22093  |
|  4 | mimo                   |          2000 |         4.0515  |               240.35  | 2016-08-19 21:15:07 | 2023-03-24 18:02:54 |                   0.6345   |                         0 |                   0.3655   |
|  5 | programming-hero       |           131 |         4.48092 |               108.122 | 2020-03-17 13:17:39 | 2023-03-22 16:03:50 |                   0.78626  |                         0 |                   0.21374  |
|  6 | programming-hub        |           867 |         4.31142 |               137.641 | 2015-12-10 13:33:31 | 2023-03-19 00:52:42 |                   0.733564 |                         0 |                   0.266436 |
|  7 | python-x               |            19 |         4.26316 |               302.737 | 2021-05-15 16:09:45 | 2023-01-07 08:25:53 |                   0.66745  |                         0 |                   0.33255  |
|  8 | sololearn              |          1702 |         4.15335 |               209.387 | 2017-10-25 19:25:02 | 2023-03-25 13:26:02 |                   0.414376 |                         0 |                   0.585624 |

---

**Spanish Reviews**

*Google Play Store Reviews*

|    | Name                   |   ReviewCount |   AverageRating |   AverageReviewLength | EarliestDate        | LatestDate          |   PositiveReviewProportion |   NeutralReviewProportion |   NegativeReviewProportion |
|---:|:-----------------------|--------------:|----------------:|----------------------:|:--------------------|:--------------------|---------------------------:|--------------------------:|---------------------------:|
|  0 | codeacademy            |           141 |         4.04255 |               78.0426 | 2019-05-05 02:40:44 | 2023-03-21 19:53:03 |                   0.567376 |                  0.219858 |                  0.212766  |
|  1 | datacamp               |           389 |         4.65553 |               87.1208 | 2018-01-27 02:54:15 | 2023-05-01 16:35:48 |                   0.786632 |                  0.125964 |                  0.0874036 |
|  2 | learn-python-programiz |            28 |         4.32143 |               92.4643 | 2020-01-04 15:02:16 | 2023-04-18 23:24:33 |                   0.642857 |                  0.321429 |                  0.0357143 |
|  3 | mimo                   |          9253 |         4.38085 |               85.0695 | 2018-06-22 22:18:37 | 2023-05-07 13:09:01 |                   0.667891 |                  0.219929 |                  0.11218   |
|  4 | programming-hero       |           221 |         4.52489 |               97.7738 | 2019-02-16 00:40:53 | 2023-04-10 06:35:09 |                   0.728507 |                  0.167421 |                  0.104072  |
|  5 | programming-hub        |          1633 |         4.2572  |               90.6852 | 2014-01-12 19:12:51 | 2023-05-06 04:27:37 |                   0.613595 |                  0.272505 |                  0.113901  |
|  6 | sololearn              |         28876 |         4.75121 |               77.0749 | 2016-10-26 07:25:37 | 2023-05-07 06:32:18 |                   0.809877 |                  0.140047 |                  0.0500762 |
