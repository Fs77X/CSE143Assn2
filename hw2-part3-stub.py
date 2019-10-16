import re
import nltk
import argparse
from nltk.corpus import stopwords
from nltk.probability import ConditionalFreqDist, FreqDist
from nltk.util import bigrams
import operator
from contextlib import redirect_stdout


def get_score(review):
    return int(re.search(r'Overall = ([1-5])', review).group(1))


def get_text(review):
    return re.search(r'Text = "(.*)"', review).group(1)


def read_reviews(file_name):
    """
    Dont change this function.

    :param file_name:
    :return:
    """
    file = open(file_name, "rb")
    raw_data = file.read().decode("latin1")
    file.close()

    positive_texts = []
    negative_texts = []
    first_sent = None
    for review in re.split(r'\.\n', raw_data):
        overall_score = get_score(review)
        review_text = get_text(review)
        if overall_score > 3:
            positive_texts.append(review_text)
        elif overall_score < 3:
            negative_texts.append(review_text)
        if first_sent == None:
            sent = nltk.sent_tokenize(review_text)
            if (len(sent) > 0):
                first_sent = sent[0]
    return positive_texts, negative_texts, first_sent


########################################################################
# Dont change the code above here
######################################################################


def process_reviews(file_name):
    positive_texts, negative_texts, first_sent = read_reviews(file_name)

    print(first_sent)

    # There are 150 positive reviews and 150 negative reviews.
    # print(len(positive_texts))
    # print(len(negative_texts))

    # Your code goes here
    pattern = '(?:\w+)?(?:[_]{0,1}\w+)?(?:[\']{0,1}\w+)'
    pos_rev = []
    neg_rev = []
    for sent in positive_texts:
        pos_rev.append(re.findall(pattern, sent))

    for sent in negative_texts:
        neg_rev.append(re.findall(pattern, sent))

    pos_rev_words = []
    neg_rev_words = []
    for review in pos_rev:
        for word in review:
            pos_rev_words.append(word.lower())

    for review in neg_rev:
        for word in review:
            neg_rev_words.append(word.lower())

    print(len(pos_rev_words))
    print(len(neg_rev_words))
    stop = stopwords.words('english')
    pos_noStop = [w for w in pos_rev_words if w not in stop]
    neg_noStop = [w for w in neg_rev_words if w not in stop]
    print(len(pos_noStop))
    print(len(neg_noStop))

    fDistPos, fDistNeg = FreqDist(), FreqDist()
    for word in pos_noStop:
        fDistPos[word] += 1

    for word in neg_noStop:
        fDistNeg[word] += 1

    dict4Pos = {}
    dict4Neg = {}

    for word in fDistPos:
        dict4Pos[word] = fDistPos[word]

    for word in fDistNeg:
        dict4Neg[word] = fDistNeg[word]

    sorted_dPos = list(sorted(dict4Pos.items(), key=operator.itemgetter(1)))
    sorted_dPos.reverse()

    sorted_dNeg = list(sorted(dict4Neg.items(), key=operator.itemgetter(1)))
    sorted_dNeg.reverse()

    fileOut = open('positve-word-freq.txt', 'w')
    for word in sorted_dPos:
        fileOut.write(word[0] + ' ' + str(word[1]) + '\n')

    fileOut.close()
    fileOut = open('negative-word-freq.txt', 'w')
    for word in sorted_dNeg:
        fileOut.write(word[0] + ' ' + str(word[1]) + '\n')

    fileOut.close()

    bigramPos = list(bigrams(pos_noStop))
    bigramNeg = list(bigrams(neg_noStop))

    cfdistPos = ConditionalFreqDist(bigramPos)
    cfdistNeg = ConditionalFreqDist(bigramNeg)
    fileOut = open('positive-bigram-freq.txt', 'w') 
    with redirect_stdout(fileOut):
        cfdistPos.tabulate()
    fileOut.close()

    fileOut = open('negative-bigram-freq.txt', 'w') 
    with redirect_stdout(fileOut):
        cfdistNeg.tabulate()
    fileOut.close()

    posText = nltk.Text(pos_noStop)
    negText = nltk.Text(neg_noStop)

    print('pos text ' + '; '.join(posText.collocation_list()))
    print('pos text ' + '; '.join(negText.collocation_list()))

    # posText.collocations()
    # negText.collocations()



# Write to File, this function is just for reference, because the encoding matters.
def write_file(file_name, data):
    # or you can say encoding="latin1"
    file = open(file_name, 'w', encoding="utf-8")
    file.write(data)
    file.close()


def write_unigram_freq(category, unigrams):
    """
    A function to write the unigrams and their frequencies to file.

    :param category: [string]
    :param unigrams: list of (word, frequency) tuples
    :return:
    """
    uni_file = open("{0}-unigram-freq-n.txt".format(category),
                    'w', encoding="utf-8")
    for word, count in unigrams:
        uni_file.write("{0:<20s}{1:<d}\n".format(word, count))
    uni_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Assignment 2')
    parser.add_argument('-f', dest="fname",
                        default="restaurant-training.data",  help='File name.')
    args = parser.parse_args()
    fname = args.fname

    process_reviews(fname)
