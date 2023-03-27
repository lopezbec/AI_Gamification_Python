# Machine Learning and Gamification for a personalized-adaptive educational application 
**[Inteligencia Artificial y Gamificación Personalizada-Adaptativa para la Formación en Programación]**
[Website of the project](https://sites.lafayette.edu/lopezbec/projects/machine-learning-and-gamification-for-a-personalized-adaptive-educational-application/)
## Abstract

This project is supported by the National Fund for Innovation and Scientific and Technological Development (FONDOCyT for its acronym in Spanish) from the Ministry of Higher Education, Science, and Technology of the Dominican Republic (**FONDOCYT 2022-3A1-112**), and is in collaboration with the Universidad Nacional Pedro Henríquez Ureña (UNPHU) and the  Asociación para la Creatividad, Innovación, Emprendimiento y Networking (A100%) from the Dominican Republic.

The project aims to explore the implementation of Machine Learning algorithms in a gamified educational application to personalize its game elements and adapt its pedagogical content.  The application will focus on helping its users learn to program using Python since Python Software Developers are among the most in-demand emerging professions. The application will implement Machine Learning algorithms to offer optimal scaffolding learning to students. This is by implementing interactive and individualized content capable of adapting to the level of knowledge and learning pace of the users. Nevertheless, the positive effects of an intelligent learning system on the learning of its users depend directly on their level of engagement and motivation. An effective method to increase user engagement and motivation in learning applications is by using gamification. Unfortunately, gamifying an application does not ensure that it will motivate all its users since the preference for game elements differs significantly between individuals. Therefore, to maximize the motivation of the users, this proposal seeks to leverage Recommendation Systems to personalize its game elements.

___________________________________________________

#  Code, Algorithms, and Models implementation
___________________________________________________

## Google Play and Apple Store App Reviews Scrapping

<table align="left">
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/lopezbec/AI_Gamification_Python/blob/main/appreviews.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Apps Reviews Scrapping</a>
  </td>
</table>
<br></br>

This project allows you to gather reviews from any app that is found on Google Play or AppStore. It lets you choose multiple options, from gathering specific number of reviews, to specify the rating of desire from the app.
The google collab grants you via forms, a visual cue of how the reviews are gathered and are saved specifically.

___________________________________________________

#  Prototype of Application   
___________________________________________________

## Example of Application Pedagogical Interface

This is a example of the "pedagogical page" (v 3_24_23)

<img src="https://github.com/lopezbec/AI_Gamification_Python/blob/main/Elmer_Pages_That_Mimic_SoloLearn/pedagogical_page.png" width="600" height="300">


## Example of Application Hexad Player type and User Data Interface


___________________________________________________

#  Data and more
___________________________________________________

|    | Name                   |   ReviewCount |   AverageRating |   AverageReviewLength | EarliestDate        | LatestDate          |
|---:|:-----------------------|--------------:|----------------:|----------------------:|:--------------------|:--------------------|
|  0 | codeacademy            |          3573 |         3.75679 |               88.5111 | 2018-08-01 01:33:12 | 2023-03-24 22:07:12 |
|  1 | datacamp               |          7719 |         4.47882 |               76.3427 | 2017-10-18 11:23:14 | 2023-03-24 21:09:12 |
|  2 | encode                 |          2045 |         4.63081 |               91.6729 | 2016-03-13 23:11:32 | 2023-03-19 01:47:34 |
|  3 | learn-python-programiz |          4814 |         4.65351 |               60.813  | 2019-08-22 19:39:09 | 2023-03-25 13:34:31 |
|  4 | mimo                   |         88724 |         4.53408 |               63.2995 | 2016-08-19 21:15:07 | 2023-03-25 15:45:02 |
|  5 | programming-hero       |         16538 |         4.78069 |               57.0992 | 2018-11-28 09:32:14 | 2023-03-25 14:57:48 |
|  6 | programming-hub        |         49549 |         4.58268 |               60.9126 | 2013-07-31 05:45:19 | 2023-03-25 14:57:25 |
|  7 | sololearn              |        132553 |         4.71747 |               61.8462 | 2016-10-26 02:56:32 | 2023-03-25 16:36:13 |