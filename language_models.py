from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.corpus import stopwords
stopset = list(set(stopwords.words('english')))
from os import listdir
from os.path import isfile, join
import pickle
import os.path

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
    # print examples
    return examples

def get_opinions():
    examples = []
    mypath = "Datasets/Raw/review_polarity/txt_sentoken/pos"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))][:5000]
    for file in onlyfiles:
        with open(join(mypath, file), "r") as f:
            for line in f.readlines():
                examples.append((word_feats(line), "opinion"))
    # print examples
    return examples

def get_data():
    train_portion = .8
    facts = get_facts()
    n_train_facts = int(train_portion * len(facts))

    opinions = get_opinions()
    n_train_opinions = int(train_portion * len(opinions))

    train_facts = facts[:n_train_facts]
    train_opinions = opinions[:n_train_opinions]

    test_facts = facts[n_train_facts:]
    test_opinions = opinions[n_train_opinions:]

    return (train_facts, train_opinions, test_facts, test_opinions)

def generate_classifier(training_data):
    classifier = NaiveBayesClassifier.train(training_data)
    return classifier

def get_classifer():
    pkl_file = "model.pkl"
    if os.path.exists(pkl_file):
        print "Reusing model file"
        with open(pkl_file) as f:
            classifier = pickle.load(f)
            return classifier
    else:
        train_facts, train_opinions, test_facts, test_opinions = get_data()
        print "Generating model file afresh"
        classifier = generate_classifier(train_facts + train_opinions)
        with open(pkl_file, "wb") as f:
            pickle.dump(classifier, f)
        return classifier

if __name__ == "__main__":
    train_facts, train_opinions, test_facts, test_opinions = get_data()
    classifier = get_classifer()

    print 'accuracy:', accuracy(classifier, test_facts + test_opinions)
    classifier.show_most_informative_features()
