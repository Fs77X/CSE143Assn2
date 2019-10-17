from nltk.corpus import wordnet as wn
from contextlib import redirect_stdout

# http://stevenloria.com/tutorial-wordnet-textblob/
# http://www.nltk.org/howto/wordnet.html
# http://wordnetweb.princeton.edu/perl/webwn


def print_syn_lemmas(word):

    ## Synsets and Lemmas
    print("1. Synsets and Lemmas")
    print("Word: " + word)
    print("")
    print("Synsets:")
    [print(s) for s in wn.synsets(word)]
    print("")
    first_synset = wn.synsets(word)[0]
    print("First synset: " + str(first_synset))
    print("")

    #word_synset = wn.synset("dog.n.01")
    print("Lemma names: ")
    [print(l) for l in first_synset.lemma_names()]
    print("")
    last_lemma = first_synset.lemmas()[len(first_synset.lemma_names())-1]
    #word_lemma = wn.lemma("dog.n.01.domestic_dog")
    print("Last lemmas: " + str(last_lemma))
    print("")
    print("Synset of Last lemmas: " + str(last_lemma.synset()))
    print("")
    for synset in wn.synsets(word):
        print(str(synset) + ": lemma_name" + str(synset.lemma_names()))
    print("")
    print("Lemmas of {}:".format(word))
    [print(l) for l in wn.lemmas(word)]
    print("")
    print("")


def print_def_exp(synset):
    ## Definitions and Examples
    print("2. Definitions and Examples")
    print("Synset: " + str(synset))
    print("Definition: " + synset.definition())
    print("")
    print("Example: " + str(synset.examples()))
    print("")
    print("Synsets of first lemma " + str(synset.lemma_names()[0]) + ": ")
    for synset in wn.synsets(synset.lemma_names()[0]):
        print(synset, ": definition (", synset.definition() + ")")
    print("")
    print("")


def print_lexical_rel(synset):
    # Lexical Relations
    print("3. Lexical Relations")
    print("Synset: " + str(synset))
    print("")
    print("Hypernyms: " + str(synset.hypernyms()))
    print("")
    print("Hyponyms: " + str(synset.hyponyms()))
    print("")
    print("Root hypernyms: " + str(synset.root_hypernyms()))
    print("")

    paths = synset.hypernym_paths()
    print("Hypernym path length of {} = {} ".format(
        str(synset), str(len(paths))))
    print("")
    for i in range(len(paths)):
        print("Path[{}]:".format(i))
        [print(syn.name()) for syn in paths[i]]
        print("")
    print("")

def getKey(item):
    return item[2]

def highest_path_similarity(data):
    lookSol = []
    for i in range(0, len(data)):
        for j in range(1, len(data)):
            if i != j:
                lookSol.append((data[i], data[j], wn.path_similarity(wn.synset(data[i]), wn.synset(data[j]))))
    
    lookSol = sorted(lookSol, key=getKey, reverse = True)
    print(lookSol)
    maxScore = lookSol[0][2]
    i = 1
    currScore = lookSol[i][2]
    sol = []
    sol.append((lookSol[0][0], lookSol[0][1]))
    #while score is max, for pair in sol, check if words different then
    counter = 0 
    while currScore == maxScore:
        for pair in sol:
            if pair[0] != lookSol[i][1] and pair[1] != lookSol[i][0] and pair[0] != lookSol[i][0] and pair[1] != lookSol[i][1]:
                counter = counter + 1
            

        if counter == len(sol):
            sol.append((lookSol[i][0], lookSol[i][1]))

        i = i + 1
        currScore = lookSol[i][2]
        counter = 0

    print('Best path similarity: ')
    for solution in sol:
        print(solution[0] + ' ' + solution[1])
    


    




def print_other_lexical_rel():
    good1 = wn.synset('good.a.01')
    wn.lemmas('good')
    print("Antonyms of 'good': " + str(good1.lemmas()[0].antonyms()))
    print("")
    print("Entailment of 'walk': " + str(wn.synset('walk.v.01').entailments()))
    print("")


if __name__ == '__main__':
    fileOut = open('wordnet.txt', 'w') 
    with redirect_stdout(fileOut):
        print_syn_lemmas('cock')
        print_def_exp(wn.synset("cock.n.01"))
        print_lexical_rel(wn.synset("cock.n.01"))
        cock = wn.synset('cock.n.01')
        ball = wn.synset('ball.n.05')
        print('Path similarity between w1 (cock) and w2 (ball), is: ' +
                str(wn.path_similarity(cock, ball)))
        stuff = ['dog.n.01', 'man.n.01', 'whale.n.01',
                    'bark.n.01', 'cat.n.01']
        highest_path_similarity(stuff)

    fileOut.close()
    
    # print_syn_lemmas('ball')
    # print_def_exp(wn.synset("ball.n.05"))
    # print_lexical_rel(wn.synset("ball.n.05"))
    # print_other_lexical_rel()
