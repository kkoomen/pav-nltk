#!/usr/bin/env python3

import json
import random
from nltk.tokenize.punkt import string
from stanfordcorenlp import StanfordCoreNLP
import sexpdata
import sys
from nltk.grammar import CFG
from nltk.parse.generate import generate
import re

# Start the Stanford CoreNLP client.
nlp = StanfordCoreNLP('http://localhost', port=9000)

# Custom types.
Rules = dict[str, list[list[str]]]
RuleGroups = dict[str, Rules]

def parse_tree_to_rules(tree: list[sexpdata.Symbol], rule_groups: RuleGroups):
    """
    Parse a given S-expression tree, loaded by the sexpdata module.

    :param tree: A list of symbols, representing the parse tree.
    :param rules: Dictionary containing all the rules.
    """
    if isinstance(tree, sexpdata.Symbol):
        return str(tree)

    lhs = get_constituent_label(str(tree[0]))

    if len(tree) > 1:
        if isinstance(tree[1], list):
            if lhs not in rule_groups['phrase_structure_rules']:
                rule_groups['phrase_structure_rules'][lhs] = []

            rhs = [get_constituent_label(str(child[0])) for child in tree[1:] if isinstance(child[0], sexpdata.Symbol)]
            if len(rhs) and rhs not in rule_groups['phrase_structure_rules'][lhs]:
                rule_groups['phrase_structure_rules'][lhs].append(rhs)

        elif not isinstance(tree[1], list) and lhs not in rule_groups['lexical_rules']:
            rule_groups['lexical_rules'][lhs] = []

    for child in tree[1:]:
        if not isinstance(child, list):
            # At this point we reached a leaf node.
            leaf_node_value = f"'{child[0]}" if isinstance(child, sexpdata.Quoted) else str(child)
            if [leaf_node_value] not in rule_groups['lexical_rules'][lhs]:
                rule_groups['lexical_rules'][lhs].append([leaf_node_value])
        else:
            parse_tree_to_rules(child, rule_groups)

def extract_rules_from_tree(parse_tree_str: str, rule_groups: RuleGroups):
    """
    Extract all the rules, given an S-expression nltk parse tree.

    :param parse_tree_str: The S-expression parse tree.
    :param rules: Dictionary containing all the rules.
    """
    parse_tree = sexpdata.loads(parse_tree_str)[1]
    parse_tree_to_rules(parse_tree, rule_groups)

def convert_rules_to_grammar_string(rules: Rules, quote_rhs: bool) -> str:
    """
    Convert a dictionary of rules to a grammar string, which can be used for any
    nltk grammar .tostring() function.

    :param rules: The rules dictionary.
    :return: The grammar string.
    """
    grammar_string = ''

    for lhs, rhs_list in rules.items():
        for rhs in rhs_list:
            if quote_rhs:
                rhs_values = ' '.join([f'"{string}"'for string in rhs])
            else:
                rhs_values = ' '.join(rhs)

            grammar_string += f"{lhs} -> {rhs_values}\n"

    return grammar_string

def generate_grammar_rules(items: list[str], is_wordlist=False) -> RuleGroups:
    """
    Generate all the grammar rules for a list of sentences.

    :param items: The list of sentences or words to generate the grammar for.
    :return: The grammar string.
    """
    rules = {
        'phrase_structure_rules': {},
        'lexical_rules': {}
    }

    if is_wordlist:
        for word in items:
            result = json.loads(nlp.annotate(word))
            for obj in result['sentences']:
                # Extract grammar rules from the parse tree string.
                extract_rules_from_tree(obj['parse'], rules)
    else:
        # list of sentences
        result = json.loads(nlp.annotate('\n'.join(items)))
        for obj in result['sentences']:
            # Extract grammar rules from the parse tree string.
            extract_rules_from_tree(obj['parse'], rules)

    return rules

def get_constituent_label(label: str) -> str:
    """
    Get a proper constituent label for a given production label.

    :param label: production label coming from a parse tree.
    :return: new constituent label.
    """
    if label in '!.?':
        return 'TABSTOP'
    elif label in string.punctuation:
        return 'PUNC'
    else:
        return re.sub(r"[^\w\d']+", '', label)

def read_phrase_structure_corpus(filename: str) -> list[str]:
    """
    Read the given filename parameter line by line and returns a list of all the
    words in the file.
    """
    return [line.strip().lower() for line in open(filename, 'r').readlines()]

def read_lexical_corpus(filename: str) -> list[str]:
    """
    Read the given filename parameter line by line and returns a list of all the
    words in the file.
    """
    with open(filename, 'r') as file:
        corpus = []
        for line in file:
            words = line.split(',')
            for word in words:
                corpus.append(word.strip().lower())
        return corpus

def format_sentence(sentence: str) -> str:
    """
    Format a generated sentence by removing leading spaces before some
    punctuation characters.

    :param sentence: Generated sentence.
    :return: Filtered sentence.
    """
    return re.sub(r" (\.|,|!|\?|')", "\\1", sentence)

def generate_samples(grammar, n: int) -> list[str]:
    """
    Generate n-sentences given a grammar.

    :param grammar: grammar instance.
    :param n: number which indicates the amount of sentence to generate.
    :return: list of sentences induced from grammar.
    """
    sentences = []
    for _ in range(n):
        frags = []
        generate_sample(grammar, grammar.start(), frags)
        sentences.append(format_sentence(' '.join(frags)))
    return sentences

def generate_sample(grammar, prod, frags):
    """
    Generate a random sentence given a grammar and some productions.

    :param grammar: grammar instance.
    :param prod list: production values.
    :param frags list[str]: contains all the fragments for a single sentence.
    """
    if prod in grammar._lhs_index:
        derivations = grammar._lhs_index[prod]
        derivation = random.choice(derivations)
        for d in derivation._rhs:
            generate_sample(grammar, d, frags)
    elif prod in grammar._rhs_index:
        # terminal
        frags.append(str(prod))

def main():
    if len(sys.argv) < 3:
        print('Usage: ./main.py FILEPATH1 FILEPATH2')
        sys.exit(1)

    print('='*80)
    print('NLTK project, gemaakt door Kim Koomen en Gijs Schouten')
    print('='*80)

    print('- Reading input files...')
    phrase_structure_corpus = read_phrase_structure_corpus(sys.argv[1])
    lexical_corpus = read_lexical_corpus(sys.argv[2])
    sentences_to_generate = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    print('- Parsing text and generating grammer rules, this might take a while...')
    print('    - Starting to generate phrase structure grammar rules')
    ps_rules = generate_grammar_rules(phrase_structure_corpus)
    phrase_structure_grammar_rules = ps_rules['phrase_structure_rules']

    print('    - Starting to generate lexical grammar rules')
    lexical_grammar_rules = generate_grammar_rules(lexical_corpus, True)['lexical_rules']

    # Regarding the third line in the array below, we're adding the words from
    # the phrase structure corpus as a backup below the lexical corpus. This
    # way, it fill first use the homophones and any leftover LHS productions
    # will be expanded to those defined in the lexical rules of the corpus used
    # for the phrase structure.
    grammar_string = '\n'.join([
        convert_rules_to_grammar_string(phrase_structure_grammar_rules, False),
        convert_rules_to_grammar_string(lexical_grammar_rules, True),
        convert_rules_to_grammar_string(ps_rules['lexical_rules'], True),
    ])

    print('- Creating CFG from generated grammar rules...')
    grammar = CFG.fromstring(grammar_string)

    print('- Generating sentences...')
    sentences = generate_samples(grammar, n=sentences_to_generate)

    print('\nDone! 🎉  Here are the generated sentences:')
    for index, sentence in enumerate(sentences):
        print(f'{index+1}) {sentence}')

if __name__ == '__main__':
    main()
