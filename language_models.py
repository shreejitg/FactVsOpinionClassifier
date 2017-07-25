from nltk.classify import NaiveBayesClassifier
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
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))][:100]
    for file in onlyfiles:
        with open(join(mypath, file), "r") as f:
            for line in f.readlines():
                examples.append((word_feats(line), "opinion"))
    print examples
    return examples

if __name__ == "__main__":
    facts = get_facts()
    opinions = get_opinions()

    classifier = NaiveBayesClassifier.train(facts + opinions)
    print classifier.classify(word_feats("This was made yesterday"))
    print classifier.classify(word_feats("Significant tension"))
    print classifier.classify(word_feats("Obamacare is a horrible decision"))
    # classifier.show_most_informative_features()