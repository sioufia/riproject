from index_inverse.index_inverse_CACM.construction_index_cacm_class import ConstructionIndex

import operator

class Search():
    def __init__(self, request):
        if not isinstance(request, str):
            raise TypeError("La requête doit être une chaîne de caractère")

        self.request = request
    
    def display_docs(postings, type_of_search):
        """Method that displays the document number of postings list"""
        if len(postings) == 0:
            print ("No results found")
        i = 1
        if type_of_search == "vector":
            for doc in postings:
                print("Result {0} : Document {1} with score {2} ".format(i, doc[0], doc[1]))
                i += 1

        elif type_of_search == "boolean":
            for doc in postings:
                print("Result {0} : Document {1} ".format(i, doc[0]))
                i += 1

class SearchBoolean(Search):
    def __init__(self, request):
        Search.__init__(self, request)
        self.request = request.split()
    
    def operator_action(postings1, operator, postings2):
        if not isinstance(postings1, list):
            raise TypeError("Les postings doivent être sous le format liste")
        if not isinstance(postings2, list):
            raise TypeError("Les postings doivent être sous le format liste")
        
        set_postings1 = set(postings1)
        set_postings2 = set(postings2)

        if operator == "AND":
            return list(set_postings1.intersection(set_postings2))

        if operator == "OR":
            return list(set_postings1.union(set_postings2))

        if operator == "NOT":
            return list(set_postings1.difference(set_postings2))
    
    def do_search(self):
        """Method that that takes an index and a search object and return the fusion of the different postings"""
        allowed_operators = ['AND', 'OR', 'NOT']
        current_fusion = index.get_termeid_postings(self.request[0])
        i = 1
        while i < len(self.request):
            if self.request[i] in allowed_operators:
                try:
                    current_fusion = SearchBoolean.operator_action(current_fusion, self.request[i], index.get_termeid_postings(self.request[i+1]))
                    i += 2
                except IndexError:
                    #Case where the request is finished by an operator
                    return current_fusion
            else:
                #case where 2 strings are not seperated by an operator. It is considered as AND
                current_fusion = SearchBoolean.operator_action(current_fusion, 'AND', index.get_termeid_postings(self.request[i]))
                i += 1
        
        return current_fusion

class SearchVector(Search):
    def __init__(self, request):
        Search.__init__(self, request)
        self.request = {'q': self.request}

    def construct_index_search(self):
        index_inverse_search = ConstructionIndex(collection_dic = self.request)
        index_inverse_search.segmenter()
        index_inverse_search.traiter_tokens_collection("CACM/common_words")
        nb_doc = index_inverse_search.index_inverse()
        index_inverse_search.weight_calculation_index(nb_doc)
        print (index_inverse_search.D_terme_termeid)
        return index_inverse_search

    def do_search(self, index_collection, k="no_limit"):
        """Takes a inverse index and do a vectorial search. Index_inverse in an Index Object """
        #The dictionnary with the classment of the doc with their score
        sj = {}

        #Generate the index of the search request
        index_inverse_search = self.construct_index_search()

        index_term_termid = index_collection.D_terme_termeid
        index_termid_postings = index_collection.D_terme_id_postings

        for term_request in index_inverse_search.D_terme_termeid:
            #get the postings of the term_request in the index
            
            postings = index_collection.get_termeid_postings(term_request)
            if len(postings) > 0:
                for doc in postings:
                    if doc in sj:
                        sj[doc] += postings[doc] * index_inverse_search.D_terme_id_postings[index_inverse_search.D_terme_termeid[term_request]]['q']
                    else:
                        sj[doc] = postings[doc] * index_inverse_search.D_terme_id_postings[index_inverse_search.D_terme_termeid[term_request]]['q']
        
        sorted_sj = sorted(sj.items(), key=operator.itemgetter(1), reverse=True)
        if k == "no_limit":
            return sorted_sj
        else:
            return sorted_sj[:k]
        
             












        