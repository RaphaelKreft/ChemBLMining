from chembl_api import get_targets_for_compound
from chembl_api import get_approved_drugs
from chembl_api import get_association_num_for_targets

from uniprot_api import get_keywords_for_accession_number

import pprint
from collections import defaultdict
import numpy as np
import pickle


def print_n(drug_queryset, n=10):
    for i, drug in enumerate(drug_queryset):
        if i > n:
            break
        pprint.pprint(drug)


def keyword_count(keyword_list, counter_dict):
    for keyword in keyword_list:
        counter_dict[keyword] += 1


if __name__ == "__main__":
    print("--All approved drugs ordered by fist approval date and id--")
    drugs = get_approved_drugs()
    print_n(drugs, 1)
    print(f"-> Overall there exist {len(drugs)} such drugs!")

    print("--Drugs approved since 2012--")
    drugs_since_2012 = get_approved_drugs(since_2012=True)
    print(f"-> Overall there exist {len(drugs_since_2012)} such drugs!")

    # For now use simple map structure, can be extended to Database
    # Map-Entries have format: compound_ID -> {(target_id, accession-number), ...}
    drug_target_map = defaultdict(set)
    target_set = set()

    # drug target map only contains values for that we can find associated targets
    for i, drug in enumerate(drugs_since_2012):
        print(f"processing drug {i} of {len(drugs_since_2012)}")
        key = drug['molecule_chembl_id']
        # now add targets
        targets = get_targets_for_compound(key)
        for target in targets:
            target_id = target['target_chembl_id']
            target_set.add(target_id)
            drug_target_map[key].add(target_id)

    # Calculate median number of targets per compound
    pprint.pprint(drug_target_map)
    num_targets_per_compound = [len(t_list) for t_list in drug_target_map.values()]

    pickle.dump(drug_target_map, open("dt_map.p", "wb"))
    pickle.dump(target_set, open("t_set.p", "wb"))

    median = np.median(num_targets_per_compound)
    print(f"Median Number of targets per compound: {median}")
    print(f"Overall we got {len(target_set)} targets!")

    # get keywords for targets
    print(f"Now getting keywords and accession number for every target!")
    target_keyword_map = dict()
    keyword_counter = defaultdict(int)
    for i, target_id in enumerate(target_set):
        print(f"Process target {i}")
        accession_num = get_association_num_for_targets(target_id)
        if accession_num is not None:
            try:
                keywords = get_keywords_for_accession_number(accession_num)
                target_keyword_map[target_id] = keywords
                keyword_count(keywords, keyword_counter)
            except Exception:
                continue

    print(f"We could found {len(target_keyword_map.keys())} targets with accession numbers! (Only for these keywords can be received)")
    print(f"The keywords that are mostly associated with targets are: {sorted(keyword_counter.items(), key=lambda x: x[1], reverse=True)}")



