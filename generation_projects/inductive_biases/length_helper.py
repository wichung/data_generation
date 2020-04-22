from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.exceptions import LengthHelperError
import random

class LengthHelper:
    def __init__(self):
        # self.antecedents = {}
        # self.adverbs = get_all("category_2", "subordinating_conj")
        # self.long_length = 18

        # self.safe_animate_common_nouns = np.setdiff1d(np.intersect1d(all_common_nouns, all_animate_nouns), get_all("expression", "doctor"))
        # self.singular_dets = get_all(get_matched_by(get_all("expression", "doctor"), "arg_1"), get_all("category_2", "D"))


    def build_dependent_clauses(self, main_clause, other_main_clause=None):
        adverb = choice(self.adverbs)
        min_long_clause_length = self.long_length - min([len(main_clause.split()), len(other_main_clause.split())]) - len(adverb[0].split())
        max_short_clause_length = self.long_length - max([len(main_clause.split()), len(other_main_clause.split())]) - len(adverb[0].split()) - 1
        short_sentences = [self.antecedents[i] for i in filter(lambda n: n <= max_short_clause_length, self.antecedents.keys())]
        # short_sentences = [s for sublist in short_sentences for s in sublist]
        if len(short_sentences) > 0:
            short_subordinate_clause = random.choice(short_sentences)
            del self.antecedents[len(short_subordinate_clause[0].split())]
        else:
            short_subordinate_clause = None
        iters = 0
        while short_subordinate_clause is None and iters <= 10:
            iters += 1
            new_sentence = make_sentence(allow_recursion=True)
            new_sentence[0] = adverb[0] + " " + new_sentence[0]
            new_sentence_length = len(new_sentence[0].split())
            if new_sentence_length <= max_short_clause_length:
                short_subordinate_clause = new_sentence
            else:
                if new_sentence_length not in self.antecedents.keys():
                    self.antecedents[new_sentence_length] = new_sentence
                # else:
                #     self.antecedents[new_sentence_length] = [new_sentence]
        if iters > 10:
            raise LengthHelperError(main_clause, "too long")

        long_sentences = [self.antecedents[i] for i in filter(lambda n: n >= min_long_clause_length, self.antecedents.keys())]
        # long_sentences = [s for sublist in long_sentences for s in sublist]
        if len(long_sentences) > 0:
            long_subordinate_clause = random.choice(long_sentences)
            del self.antecedents[len(long_subordinate_clause[0].split())]
        else:
            long_subordinate_clause = None
        iters = 0
        while long_subordinate_clause is None and iters <= 10:
            iters += 1
            new_sentence = make_sentence(allow_recursion=True)
            new_sentence[0] = adverb[0] + " " + new_sentence[0]
            new_sentence_length = len(new_sentence[0].split())
            if new_sentence_length >= min_long_clause_length:
                long_subordinate_clause = new_sentence
            else:
                if new_sentence_length in self.antecedents.keys():
                    self.antecedents[new_sentence_length] = new_sentence
                # else:
                #     self.antecedents[new_sentence_length] = [new_sentence]
        if iters > 10:
            raise LengthHelperError(main_clause, "too short")

        return long_subordinate_clause, short_subordinate_clause

