import argparse, re, nltk
import operator

# https://docs.python.org/3/howto/regex.html
# https://docs.python.org/3/library/re.html
# https://www.debuggex.com/


def get_words(pos_sent):
    """
    Given a part-of-speech tagged sentence, return a sentence
    including each token separated by whitespace.

    As an interim step you need to fill word_list with the
    words of the sentence.

    :param pos_sent: [string] The POS tagged stentence
    :return:
    """

    pattern = '(\w+)/'

    # add the words of the sentence to this list in sequential order.
    
    word_list = re.findall(pattern, pos_sent)
    print(word_list)
    # Your code goes here

    # Write a regular expression that matches only the
    # words of each word/pos-tag in the sentence.

    # END OF YOUR CODE
    retval = " ".join(word_list) if len(word_list) > 0 else None
    return retval


def get_pos_tags(pos_sent):
    # Your code goes here
    pattern = '(\w+)'
    word_list = re.findall(pattern, pos_sent)
    print(word_list)
    getPos = []
    for i in range(len(word_list)):
        if i % 2 != 0:
            getPos.append(word_list[i])

    return getPos




def get_noun_phrases(pos_sent):
    """
    Find all simple noun phrases in pos_sent.

    A simple noun phrase is a single optional determiner followed by zero
    or more adjectives ending in one or more nouns.

    This function should return a list of noun phrases without tags.

    :param pos_sent: [string]
    :return: noun_phrases: [list]
    """

    noun_phrases = []

    # Your code goes here
    pattern = '(\w+/DT|\w+/NN)'
    DT = '(DT)'
    NN = '(NN)'
    pattwoDT = '(\w+)/DT'
    pattwoNN = '(\w+)/NN'

    noun_phrases = re.findall(pattern, pos_sent)
    print(noun_phrases)
    realNouns = []
    i = 0
    while i <= len(noun_phrases) - 1:
        print('i at: ' + str(i))
        if re.search(DT, noun_phrases[i]) and i != len(noun_phrases) - 1:
            if re.search(NN, noun_phrases[i+1]):
                realNouns.append(re.findall(pattwoDT, noun_phrases[i])[0] + ' ' + re.findall(pattwoNN, noun_phrases[i+1])[0])
                i = i + 2
            else:       #if not re.search(NN, noun_phrases[i+1])
                i = i + 1
        elif re.search(NN, noun_phrases[i]):
            realNouns.append(re.findall(pattwoNN, noun_phrases[i])[0])
            i = i + 1
        else:
            i = i + 1

    print(realNouns)
    noun_phrases = realNouns

    # END OF YOUR CODE

    return noun_phrases


def read_stories(fname):
    stories = []
    with open(fname, 'r') as pos_file:
        story = []
        for line in pos_file:
            if line.strip():
                story.append(line)
            else:
                stories.append("".join(story))
                story = []
    return stories



def most_freq_noun_phrase(pos_sent_fname, verbose=True):
    """

    :param pos_sent_fname:
    :return:
    """
    story_phrases = {}
    story_id = 1
    for story in read_stories(pos_sent_fname):
        most_common = []
        # your code starts here
        dic4Nouns = {}
        nounInStory = get_noun_phrases(story)
        for noun in nounInStory:
            dic4Nouns[noun] = nounInStory.count(noun)
        sorted_dic = list(sorted(dic4Nouns.items(), key =operator.itemgetter(1)))
        sorted_dic.reverse()
        print(sorted_dic)


        # do stuff with the story

        # end your code
        if verbose:
            print("The most freq NP in document[" + str(story_id) + "]: " + str(most_common))
        story_phrases[story_id] = most_common
        story_id += 1

    return story_phrases

def most_freq_pos_tags(pos_sent_fname, verbose=True):
    """

    :param pos_sent_fname:
    :return:
    """
    story_tags = {}
    story_id = 1
    for story in read_stories(pos_sent_fname):
        most_common = []
        # your code starts here

        # do stuff with the story

        # end your code
        if verbose:
            print("The most freq pos tags in document[" + str(story_id) + "]: " + str(most_common))
        story_tags[story_id] = most_common
        story_id += 1

    return story_tags



def test_get_words():
    """
    Tests get_words().
    Do not modify this function.
    :return:
    """
    print("\nTesting get_words() ...")
    pos_sent = 'All/DT animals/NNS are/VBP equal/JJ ,/, but/CC some/DT ' \
               'animals/NNS are/VBP more/RBR equal/JJ than/IN others/NNS ./.'
    print(pos_sent)
    retval = str(get_words(pos_sent))
    print("retval:", retval)

    gold = "All animals are equal but some animals are more equal than others"
    assert retval == gold, "test Fail:\n {} != {}".format(retval, gold)

    print("Pass")


def test_get_pos_tags():
    """
    Tests get_pos_tags().
    Do not modify this function.
    :return:
    """
    print("\nTesting get_pos_tags() ...")
    pos_sent = 'All/DT animals/NNS are/VBP equal/JJ ,/, but/CC some/DT ' \
               'animals/NNS are/VBP more/RBR equal/JJ than/IN others/NNS ./.'
    print(pos_sent)
    retval = str(get_pos_tags(pos_sent))
    print("retval:", retval)

    gold = str(['DT', 'NNS', 'VBP', 'JJ', 'CC', 'DT', 'NNS', 'VBP', 'RBR', 'JJ', 'IN', 'NNS'])
    assert retval == gold, "test Fail:\n {} != {}".format(retval, gold)

    print("Pass")



def test_get_noun_phrases():
    """
    Tests get_noun_phrases().
    Do not modify this function.
    :return:
    """
    print("\nTesting get_noun_phrases() ...")

    pos_sent = 'All/DT animals/NNS are/VBP equal/JJ ,/, but/CC some/DT ' \
               'animals/NNS are/VBP more/RBR equal/JJ than/IN others/NNS ./.'
    print("input:", pos_sent)
    retval = str(get_noun_phrases(pos_sent))
    print("retval:", retval)

    gold = "['All animals', 'some animals', 'others']"
    assert retval == gold, "test Fail:\n {} != {}".format(retval, gold)

    print("Pass")


def test_most_freq_noun_phrase(infile="fables-pos.txt"):
    """
    Tests most_get_noun_phrase().
    Do not modify this function.
    :return:
    """
    print("\nTesting most_freq_noun_phrase() ...")

    import os
    if os.path.exists(infile):
        noun_phrase = most_freq_noun_phrase(infile, False)
        gold = "[('the donkey', 6), ('the mule', 3), ('load', 2)]"
        retval = str(noun_phrase[7])

        print("gold:\t", gold)
        print("retval:\t", retval)

        assert retval == gold, "test Fail:\n {} != {}".format(noun_phrase[7], gold)
        print("Pass")
    else:
        print("Test fail: path does not exist;", infile)

def test_most_freq_pos_tags(infile="fables-pos.txt"):
    """
    Tests most_freq_pos_tags().
    Do not modify this function.
    :return:
    """
    print("\nTesting most_freq_pos_tags() ...")

    import os
    if os.path.exists(infile):
        pos_tags = most_freq_pos_tags(infile, False)
        gold = "[('DT', 28), ('NN', 24), ('IN', 21)]"
        retval = str(pos_tags[7])

        print("gold:\t", gold)
        print("retval:\t", retval)

        assert retval == gold, "test Fail:\n {} != {}".format(pos_tags[7], gold)
        print("Pass")
    else:
        print("Test fail: path does not exist;", infile)


def run_tests():
    test_get_words()
    test_get_pos_tags()
    test_get_noun_phrases()
    test_most_freq_noun_phrase()
    test_most_freq_pos_tags()


if __name__ == '__main__':

    # comment this out if you dont want to run the tests
    run_tests()

    parser = argparse.ArgumentParser(description='Assignment 2')
    parser.add_argument('-i', dest="pos_sent_fname", default="blogs-pos.txt",  help='File name that contant the POS.')

    args = parser.parse_args()
    pos_sent_fname = args.pos_sent_fname

    most_freq_noun_phrase(pos_sent_fname)

