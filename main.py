#!/usr/bin/env python3

from stanfordcorenlp import StanfordCoreNLP
import sexpdata

# Start the Stanford CoreNLP client.
nlp = StanfordCoreNLP('http://localhost', port=9000)

# Custom types.
Rules = dict[str, list[list[str]]]

def parse_tree_to_rules(tree: list[sexpdata.Symbol], rules: Rules):
    """
    Parse a given S-string tree, loaded by the sexpdata module.

    :param tree: A list of symbols, representing the parse tree.
    :param rules: Dictionary containing all the rules.
    """
    if isinstance(tree, sexpdata.Symbol):
        return str(tree)

    lhs = str(tree[0])

    if lhs not in rules:
        rules[lhs] = []

        # Append all the RHS labels to the current LHS.
        rhs = [str(symbol[0]) for symbol in tree[1:] if not isinstance(symbol, sexpdata.Symbol)]
        if len(rhs):
            rules[lhs].append(rhs)

    for child in tree[1:]:
        if isinstance(child, sexpdata.Symbol):
            # At this point we reached a leaf node.
            leaf_node_value = str(child)
            if [leaf_node_value] not in rules[lhs]:
                rules[lhs].append([leaf_node_value])
        else:
            parse_tree_to_rules(child, rules)

def extract_rules_from_tree(parse_tree_str: str, rules: Rules):
    """
    Extract all the rules, given an S-string nltk parse tree.

    :param parse_tree_str: The S-string parse tree.
    :param rules: Dictionary containing all the rules.
    """
    parse_tree = sexpdata.loads(parse_tree_str)[1]
    parse_tree_to_rules(parse_tree, rules)

def convert_rules_to_grammar_string(rules: Rules) -> str:
    """
    Convert a dictionary of rules to a grammar string, which can be used for any
    nltk grammar .tostring() function.

    :param rules: The rules dictionary.
    :return: The grammar string.
    """
    grammar_string = ''

    for lhs, rhs_list in rules.items():
        for rhs in rhs_list:
            grammar_string += f"{lhs} -> {' '.join(rhs)}\n"

    return grammar_string

def generate_grammar_rules(sentences: list[str]) -> str:
    """
    Generate all the grammar rules for a list of sentences.

    :param sentences: The list of sentences to generate the grammar for.
    :return: The grammar string.
    """
    rules = {}

    for sentence in sentences:
        # Perform the constituent parsing and obtain parse tree as a string
        parse_tree_str = nlp.parse(sentence.lower())

        # Extract grammar rules from the parse tree string.
        extract_rules_from_tree(parse_tree_str, rules)

    return convert_rules_to_grammar_string(rules)

def read_phrase_structure_corpus(filename: list) -> list[str]:
    """
    Read the given filename parameter line by line and returns a list of all the
    words in the file.
    """
    pass

def read_lexical_corpus(filename: list) -> list[str]:
    """
    Read the given filename parameter line by line and returns a list of all the
    words in the file.
    """
    pass

def main():
    # 1. Read the input filenames its contents.
    phrase_structure_corpus = read_phrase_structure_corpus('./foxinsocks.txt')
    lexical_corpus = read_lexical_corpus('./homophones.txt')

if __name__ == '__main__':
    main()
