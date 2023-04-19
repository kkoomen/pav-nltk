#!/usr/bin/env python3

def read_corpus(filename):
    """
    Read the given filename parameter line by line and returns a list of all the
    words in the file.
    """
    pass

def tag_corpus(corpus):
    """
    Use NLTK to tag the corpus.
    """
    pass

def generate_rules(tagged_corpus):
    pass

def generate_grammar(rules):
    pass

def generate_sentence(grammar):
    pass

def main():
    # 1. foxinsocks.txt inlezen
    corpus = read_corpus('./foxinsocks.txt')

    # 2. Gebruik NLTK package om de corpus te taggen.
    tagged_corpus = tag_corpus(corpus)

    # 3. Lexicon & Phrase structure rules opstellen (NLTK laten doen)
    rules = generate_rules(tagged_corpus)
    grammar = generate_grammar(rules)

    # 4. Generate sentences given the grammar
    sentence = generate_sentence(grammar)

    # 5. Print the sentence.

if __name__ == '__main__':
    main()
