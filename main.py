from chembl_api import get_targets_for_compound
from chembl_api import get_approved_drugs
from chembl_api import get_association_num_for_targets

from uniprot_api import get_keywords_for_accession_number


def print_n(drug_queryset, n=10):
    for i, drug in enumerate(drug_queryset):
        if i > n:
            break
        print(f"{drug} \n")


if __name__ == "__main__":
    print("--All approved drugs ordered by fist approval date and id--")
    drugs = get_approved_drugs()
    print_n(drugs, 3)

    print("--Drugs approved since 2012--")
    drugs_since_2012 = get_approved_drugs(since_2012=True)

    # For now use simple map structure, can be extended to Database
    # Map-Entries have format: compound_ID -> {(target_id, accession-number), ...}
    drug_target_map = dict()
    for i, drug in enumerate(drugs_since_2012):
        if i > 1:  # Just doing it for two drugs for time reasons
            break
        print(f"processing drug {i} of {len(drugs_since_2012)}")
        key = drug['molecule_chembl_id']
        # create key if not exists use set since I don't know whether there are duplicates in the database
        if key not in drug_target_map.keys():
            drug_target_map[key] = set()
        # now add targets
        targets = get_targets_for_compound(key)
        for target in targets:
            target_id = target['target_chembl_id']
            corresponding_accession_num = get_association_num_for_targets(target_id)
            drug_target_map[key].add((target_id, corresponding_accession_num))

    # Print Example target keywords -> If we wanted all, we could create a map for all targets and query all keywords by loop through targets in the drug target map.
    print(get_keywords_for_accession_number("P10275"))
