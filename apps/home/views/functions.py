from django.http import HttpResponse
from serpapi import GoogleSearch
from ..models import *
from django.db.models import F, Q

def serpapi_author(researcher_id):
    params = {
        "engine": "google_scholar_author",
        "author_id": researcher_id,
        "api_key": "016c19a111a3df750b7a37250aedf532683ef08faa73e2ab7f4aba7f2f2746be"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if "errors" in results :
        return {"api-kmel" : "api key kmel"}
    return results

def check_gs_id(gs_id):
    params = {
        "engine": "google_scholar_author",
        "author_id": gs_id,
        "api_key": "016c19a111a3df750b7a37250aedf532683ef08faa73e2ab7f4aba7f2f2746be"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if "author" in results:
        return True
    return False

def get_gs_id(account):
    return account.partition("user=")[2][:12]


def get_researcher_citations(researcher):
    author = serpapi_author(researcher.get_google_id())
    citations = 0
    if "cited_by" in author :
        citations = author["cited_by"]["table"][0]["citations"]["all"]
        print(citations)
    if "api-kmel" in author : 
        return "api key kmel"
    return citations

def get_etablisement_researchers(eta_id):
    return Researcher.objects.filter(Q(division__etablisment__id=eta_id) | Q(equipe__division__etablisment__id=eta_id) | Q(equipe_researchers__division__etablisment__id=eta_id) | Q(etablisment__id=eta_id))

def get_citations_total_etablisement(eta_id):
    total_citaions = 0
    researchers = list(get_etablisement_researchers(eta_id))
    for researcher in researchers :
        print(researcher)
        total_citaions += get_researcher_citations(researcher)
    return total_citaions
    
def get_citations_all_etablisements():
    citations = 0
    for etablisement in Etablisment.objects.all():
        citations += get_citations_total_etablisement(etablisement.id)
    return citations



def final_years_citations_etablisement(eta_id):
    pass        


