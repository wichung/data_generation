from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify


class BindingGenerator(data_generator.Generator):
    def __init__(self):
        super().__init__()
        self.all_safe_nouns = np.setdiff1d(self.all_nouns, self.all_singular_neuter_animate_nouns)
        self.all_safe_common_nouns = np.intersect1d(self.all_safe_nouns, self.all_common_nouns)

    def sample(self):
        # The woman who defeated John saw herself.
        # N1        C1  Vembed   N2   V1  refl_match

        # The woman who defeated John saw himself.
        # N1        C1  Vembed   N2   V1  refl_mismatch

        V1 = choice(self.all_refl_preds)
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_safe_common_nouns)))
        except IndexError:
            pass
        refl_match = choice(get_matched_by(N1, "arg_1", self.all_reflexives))
        # D1 = choice(get_matched_by(N1, "arg_1", self.all_common_dets))
        C1 = choice(get_matched_by(N1, "arg_1", self.all_relativizers))
        Vembed = choice(get_matched_by(N1, "arg_1", self.all_transitive_verbs))
        try:
            N2 = choice(get_matches_of(Vembed, "arg_2", self.all_safe_nouns))
        except TypeError:
            pass
        while is_match_disj(N2, refl_match["arg_1"]):
            N2 = choice(get_matches_of(Vembed, "arg_2", self.all_safe_nouns))
        N2 = N_to_DP_mutate(N2)
        # D2 = choice(get_matched_by(N2, "arg_1", self.all_common_dets))
        refl_mismatch = choice(get_matched_by(N2, "arg_1", self.all_reflexives))

        V1 = conjugate(V1, N1)
        Vembed = conjugate(Vembed, N1)

        metadata = [
            "category=agreement-field=syntax/semantics-linguistics_term=binding-UID=principle_A_c_command-crucial_item=%s" % refl_match[0],
            "category=agreement-field=syntax/semantics-linguistics_term=binding-UID=principle_A_c_command-crucial_item=%s" % refl_mismatch[0]
        ]
        judgments = [1, 0]
        sentences = [
            "%s %s %s %s %s %s." % (N1[0], C1[0], Vembed[0], N2[0], V1[0], refl_match[0]),
            "%s %s %s %s %s %s." % (N1[0], C1[0], Vembed[0], N2[0], V1[0], refl_mismatch[0])
        ]
        return metadata, judgments, sentences


binding_generator = BindingGenerator()
binding_generator.generate_paradigm(rel_output_path="outputs/benchmark/principle_A_c_command.tsv")












