from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.corpus import stopwords
stopset = list(set(stopwords.words('english')))
from os import listdir
from os.path import isfile, join

def word_feats(words):
    return dict([(word.lower(), True) for word in words.split() if word not in stopset])

def get_facts():
    examples = []
    mypath = "Datasets/Processed/Facts/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles:
        with open(join(mypath, file), "r") as f:
            for line in f.readlines():
                examples.append((word_feats(line), "fact"))
    print examples
    return examples

def get_opinions():
    examples = []
    mypath = "Datasets/Raw/review_polarity/txt_sentoken/pos"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))][:5000]
    for file in onlyfiles:
        with open(join(mypath, file), "r") as f:
            for line in f.readlines():
                examples.append((word_feats(line), "opinion"))
    print examples
    return examples

if __name__ == "__main__":
    train_portion = .8
    facts = get_facts()
    n_train_facts = int(train_portion * len(facts))

    opinions = get_opinions()
    n_train_opinions = int(train_portion * len(opinions))

    train_facts = facts[:n_train_facts]
    train_opinions = opinions[:n_train_opinions]

    test_facts = facts[n_train_facts:]
    test_opinions = opinions[n_train_opinions:]

    classifier = NaiveBayesClassifier.train(train_facts + train_opinions)

    print 'accuracy:', accuracy(classifier, test_facts + test_opinions)
    classifier.show_most_informative_features()
