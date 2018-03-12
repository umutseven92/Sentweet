# Luscinia [![Build Status](https://travis-ci.org/umutseven92/SWE573.svg?branch=master)](https://travis-ci.org/umutseven92/SWE573)
Lusicinia is a sentiment analyzer & visualizer that uses the Twitter API. This project is being built for the Software Development Practice class in the Boğaziçi University Software Engineering Masters Programme, under the supervision of Prof. Dr. Suzan Üsküdarli.

## Project Details
Lusicinia allows users to perform sentiment analysis via a web user interface. It will query the Twitter API and chart out the general feelings people have about a certain topic. The user will be able to choose a time range and a country. The results- which are the negativity score, positivity score, neutrality score and the compound score- will be displayed in a chart.

The project is written using Python 3 with Django. It uses the [NLTK](https://www.nltk.org/) library for NLP and sentiment analysis work.

### Sentiment Analysis
Sentiment analysis is done by the NLTK library. Specifically, it uses the VADER (Valence Aware Dictionary and sEntiment Reasoner) module, which is optimized for social media posts -perfect for this project. How VADER works can be read [here](http://t-redactyl.io/blog/2017/04/using-vader-to-handle-sentiment-analysis-with-social-media-text.html), however, to summarize; VADER assigns a score to each word in the sentence based on how negative or positive it is, then sums them up and returns a compound value. What makes VADER a good fit for social media texts is that it also takes emoticons, acronyms, capitalization and punctuation into account. It even considers modifier words like _extremely_ into account.

For more details about VADER, please take a look at the paper _VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text_ by C.J. Hutto Eric Gilbert from Georgia Institute of Technology, Atlanta, GA, which can be found [here](comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf). 

For more information about NLTK in general, please take a look at the NLTK book _Natural Language Processing with Python_ published by O’Reilly Media Inc. from authors Bird, Steven, Edward Loper and Ewan Klein.
