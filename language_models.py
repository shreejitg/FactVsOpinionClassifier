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

def get_raw_facts():
    examples = []
    mypath = "Datasets/Processed/Facts/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles:
        with open(join(mypath, file), "r") as f:
            for line in f.readlines():
                examples.append(line)
    # print examples
    return examples

def get_facts():
    return [(word_feats(example[0]), "fact") for example in get_raw_facts()]

def get_raw_opinions():
    examples = []
    mypath = "Datasets/Raw/review_polarity/txt_sentoken/pos"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))][:5000]
    for file in onlyfiles:
        with open(join(mypath, file), "r") as f:
            for line in f.readlines():
                examples.append(line)
    # print examples
    return examples

def get_opinions():
    return [(word_feats(example[0]), "opinion") for example in get_raw_opinions()]

def split_traintest(train_portion, facts, opinions):
    n_train_facts = int(train_portion * len(facts))

    n_train_opinions = int(train_portion * len(opinions))

    train_facts = facts[:n_train_facts]
    train_opinions = opinions[:n_train_opinions]

    test_facts = facts[n_train_facts:]
    test_opinions = opinions[n_train_opinions:]

    return (train_facts, train_opinions, test_facts, test_opinions)

def get_raw_data():
    return split_traintest(0.8, get_raw_facts(), get_raw_opinions())

def get_data():
    return split_traintest(0.8, get_facts(), get_opinions())

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

def predict(sentences):
    classifier = get_classifer()
    return [classifier.classify(word_feats(sentence)) for sentence in sentences]

if __name__ == "__main__":
    # train_facts, train_opinions, test_facts, test_opinions = get_data()
    # classifier = get_classifer()
    #
    # print 'accuracy:', accuracy(classifier, test_facts + test_opinions)
    # classifier.show_most_informative_features()

    print predict(["George Washington was the first president of the United States of America",
                   "I hate this movie"])