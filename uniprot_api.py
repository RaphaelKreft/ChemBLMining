import requests

"""
Provide Methods to retrieve Keywords associated with a certain protein/target identified
by an accession number.
"""

API_ENDPOINT = "https://www.ebi.ac.uk/proteins/api/proteins/"


def make_api_request(url: str):
    response = requests.get(url)
    if not response.ok:
        response.raise_for_status()
    else:
        return response.json()


def get_protein_data_by_accession_number(accession_num):
    return make_api_request(API_ENDPOINT + str(accession_num))


def get_keywords_for_accession_number(accession_number) -> list:
    keyword_list = get_protein_data_by_accession_number(accession_number)['keywords']
    keywords_unpacked = map(lambda x: x['value'], keyword_list)
    return list(keywords_unpacked)


if __name__ == "__main__":
    keywords = get_keywords_for_accession_number("P12345")
    print(keywords)

