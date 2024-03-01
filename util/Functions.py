from util.Global import *
import numpy as np
import Levenshtein as l



def get_data_range(data, start = 1900, end = 2100, _type = None):
    res = []
    if _type != None:
        for d in data:
            if int(d.ano) >= start and int(d.ano) <= end and d.tipo in _type:
                res.append(d)
    else:
        for d in data:
            if int(d.ano) >= start and int(d.ano) <= end:
                res.append(d)
    return res


def get_freq_based_on_year(data, _type = None):
    freq = {}
    if _type != None:
        for d in data:
            if d.tipo == _type:
                year = d.ano
                freq[year] = freq[year] + 1 if year in freq else 1
    else:
        for d in data:
            year = d.ano
            freq[year] = freq[year] + 1 if year in freq else 1
    return freq


def get_freq_based_on_qualis(data):
    freq = {}
    qualis_type = {'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C', 'NI'}
    
    for d in data:
        if d.qualis != None:
            qualis = d.qualis.upper()
            if qualis in qualis_type:            
                freq[qualis] = freq[qualis] + 1 if qualis in freq else 1
            else:
                freq['NI'] = freq['NI'] + 1 if 'NI' in freq else 1    
        else:
            freq['NI'] = freq['NI'] + 1 if 'NI' in freq else 1
        

    return freq


def equal_title(t1, t2) -> bool:
    t1 = " ".join(t1.split()).strip().upper()
    t2 = " ".join(t2.split()).strip().upper()    
    return l.distance(t1, t2) <= EDIT_DISTANCE_TITLE  
    
    
def remove_redundancy(prods):  
    prods = np.array(prods)
    mask = np.full(len(prods), True, dtype = bool)

    for i in range(len(prods) - 1):
        if mask[i]:
            for j in range(i + 1, len(prods)):
                if mask[j]:
                    if equal_title(prods[i].titulo, prods[j].titulo):
                        mask[j] = False
    
    return prods[mask], mask


def remove_redundancy_list(prods):  
    prods = np.array(prods)
    mask = np.full(len(prods), True, dtype = bool)

    for i in range(len(prods) - 1):
        if mask[i]:
            for j in range(i + 1, len(prods)):
                if mask[j]:
                    if equal_title(prods[i], prods[j]):
                        mask[j] = False
    
    return prods[mask], mask



def detect_authors(cit_ppgcc: list, authors_of_paper: list) -> list:
    res = []
    aux = {}
    paper_authors = set(authors_of_paper)
    
    for one_ppgcc in cit_ppgcc: # lista de pesquisadores
        full_name = one_ppgcc[0]
        
        for cit in one_ppgcc: # lista de citações de um pesquisador
            found = False
                            
            for cit_p in paper_authors: # lista de autores do artigo
                dist = l.distance(cit, cit_p)
                if dist <= EDIT_DISTANCE_AUTHOR_NAME:
                    found = True
                    
                    if cit_p in aux.keys():
                        if dist < aux[cit_p][0]:
                            res.pop(aux[cit_p][1])
                            res.append(full_name)
                            aux[cit_p] = [dist, len(res) - 1]                            
                    else:
                        res.append(full_name)
                        aux[cit_p] = [dist, len(res) - 1]
                    
                    break
                
            
            if found:
                break
            
                    
    return res


def extract_citations(researchers: list) -> list:
    return [r.citacoes for r in researchers]


def extract_colabs(cit_authors, papers) -> dict:
    colabs = {}
    
    for p in papers:
        authors = detect_authors(cit_authors, p.autores)
        
        for a in authors:
            colabs[a] = colabs[a] + 1 if a in colabs else 1
    
    return colabs
    
    
def build_colabs_matrix(cit_ppgcc, producoes):
    fnames = [s[0] for s in cit_ppgcc]
    colabs = pd.DataFrame(0, index = fnames, columns = fnames)
    
    for producao in producoes:
        authors = fun.detect_authors(cit_ppgcc, producao.autores)
        for author in authors:
            colabs.loc[author, authors] = colabs.loc[author, authors] + 1
    
    return colabs