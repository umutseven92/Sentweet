from .helpers import sentiment_helper as sh

# Sentences taken from http://www.nltk.org/howto/sentiment.html

sentences = {"VADER is smart, handsome, and funny.": {"comp": 0.8316, "pos": 0.746, "neg": 0.0, "neu": 0.254},
             "VADER is smart, handsome, and funny!": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "VADER is very smart, handsome, and funny.": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "VADER is VERY SMART, handsome, and FUNNY.": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "VADER is VERY SMART, handsome, and FUNNY!!!": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!!": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "The book was good.": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "The book was kind of good.": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "The plot was good, but the characters are uncompelling and the dialog is not great.": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "A really bad, horrible book.": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "At least it isn't a horrible book.": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             ":) and :D": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "Today sux": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "Today sux!": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "Today SUX!": {"comp": 0, "pos": 0, "neg": 0, "neu": 0},
             "Today kinda sux! But I'll get by, lol": {"comp": 0, "pos": 0, "neg": 0, "neu": 0}
             }


def test_can_do_basic_sent_analysis_correctly():

    for sentence, values in sentences.items():
        ss = sh.get_sentiment_scores(sentence)
        compound = ss['compound']
        pos = ss['pos']
        neg = ss['neg']
        neu = ss['neu']

        correct_compound = values["comp"]
        correct_pos = values["pos"]
        correct_neg = values["neg"]
        correct_neu = values["neu"]

        correct = compound == correct_compound and pos == correct_pos and neg == correct_neg and neu == 0.254
        assert correct
