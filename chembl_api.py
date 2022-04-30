from chembl_webresource_client.new_client import new_client


def get_approved_drugs(since_2012=False):
    drug_data_abstraction = new_client.drug
    # Max-Phase 4 means that the drug has been approved!
    approved_drugs = drug_data_abstraction.filter(max_phase=4)
    res = approved_drugs.order_by(
        ['molecule_chembl_id', 'first_approval']).only(['molecule_chembl_id', 'first_approval', 'synonyms'])
    return res.filter(first_approval__gte=2012) if since_2012 else res


def get_targets_for_compound(compound_chembl_id: str):
    target_data_abstraction = new_client.activity
    res = target_data_abstraction.filter(molecule_chembl_id=compound_chembl_id).only('target_chembl_id')
    return res


def get_association_num_for_targets(target_info):
    """
    Uses the target entity of ChemBL QuerySet new_client to get data for specific data.
    From the retrieved Data we then extract accession number and return it.
    :param target_info: One specific target_chembl_id
    :return: accession number
    """
    target_data = new_client.target
    res = target_data.filter(target_chembl_id=target_info).only('target_components')
    # from target result extract one specific component value -> accession number
    if len(res) == 0 or len(res[0]['target_components']) == 0:
        return None
    else:
        return res[0]['target_components'][0]['accession']
