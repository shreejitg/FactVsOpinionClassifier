from bs4 import BeautifulSoup
import urllib
import re
from xml.etree import ElementTree as ET


def get__great_facts():
    r = urllib.urlopen("http://www.greatfacts.com/").read()
    soup = BeautifulSoup(r, 'html.parser')
    facts = soup.find_all("table")[2].extract().find_all("tr")[1]
    text = facts.get_text()
    cleaned_text = re.sub("(<!--.*?-->)", "", text, flags=re.DOTALL)
    output = [line + '\n' for line in cleaned_text.split('\n') if len(line) > 0][:-2]
    with open("Datasets/Processed/Facts/facts1.csv", "w") as f:
        f.writelines(output)

def get_ukranian_facts():
    r = urllib.urlopen("http://www.ukraine.com/forums/open-board/8241-huge-list-interesting-but-useless-facts.html").read()
    soup = BeautifulSoup(r, 'html.parser')
    facts = soup.find_all("div", id="post_message_68738")[0].extract()
    text = facts.get_text()
    cleaned_text = re.sub("(<!--.*?-->)", "", text, flags=re.DOTALL)
    output = [(line + '\n').encode('utf-8') for line in cleaned_text.split('\n') if len(line) > 6]
    print output
    with open("Datasets/Processed/Facts/facts2.csv", "w") as f:
        f.writelines(output)

if __name__ == "__main__":
    get_ukranian_facts()