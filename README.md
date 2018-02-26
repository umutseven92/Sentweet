# SWE573
This repository is for the project that I will work on every week for the SWE 573 class, under the supervision of Prof. Dr. Suzan Uskudarli in Bogazici University.

Every week, a summary of the research I do will be posted on the wiki page of this repository. They will be titled "Week One", "Week Two" etc.

It is my hope that this repository will be kept up to date on a regular basis.

## Project Details
The project will allow users to perform sentiment analysis via a web user interface. It will query the Twitter API and chart out the general feelings people have about a certain topic. The user will be able to choose a time range and a country. The results will be displayed as charts.

The project will be written using Python 3 with Django.

### Sentiment Analysis
Sentiment analysis will be done by analyzing the tweets and assigning a score to them which signifies how positive or negative it is. A minus score will mean a negative tweet, while a positive score will mean a positive tweet. A score of zero means a tweet is neutral. The scoring will be accomplished by having a database of words that have their own scoring on how positive or negative the word is, and then adding them up.

#### Example
For example, the tweet:

>I hate that goddamn idiot. I hope he dies.

has four negative words - "hate", "goddamn", "idiot" and "dies". It also has one positive word, "hope". If we were to assign scores to these words based on how positive or negative they are, we can come up with this table (please note that for this example, the scores are arbitrary):

| Word        | Score           |
| ------------- | ------------- |
|hate| -7 |
| goddamn      | -3      |
| idiot | -3      |
| dies | -8      |
| hope | 3      |

Adding up the scores, we get -18, which means that our tweet is very negative.

#### Notes
* We will take misspelings into account.
* Intensifier words like very, too, so, quite, rather will have multipliers that affect the word to the right of them. For example, if "good" has a score of 4, and "very" has the multiplier of 2, "very good" will have the score of 8.
* Negator words like not will reverse the score. For example, if "bad" has a score of -3, "not bad" will have a score of 3.
* If possible, we will use existing word databases.
