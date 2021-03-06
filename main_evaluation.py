from evaluation.evaluation import Evaluation
from index_inverse.index_inverse_memory.index_inverse_memory_cacm.index_inverse_memory_cacm import IndexCACMMemory
import matplotlib.pyplot as plt
from statistics import mean

def get_doc_relevants_query(query_nb):
    """Method that get the relevant doc for a query from the query set"""
    L = []
    with open("CACM/qrels.text", "r") as f:
        for line in f:
            line = line.split(" ")
            if int(line[0]) > query_nb:
                break
            elif int(line[0]) == query_nb:
                L.append(int(line[1]))
        return L

def loop_query_test():
    """Method that parse the query.text file. It returns a dictionnary with query_number as key
       and query as value."""
    D = {}
    current_test_nb = 0
    current_section_list = ""
    section_list = [".I", ".N", ".W", ".A"]
    with open("CACM/query.text", "r") as f:
        for line in f:
            if line[:2] in section_list:
                current_section_list = line[:2]
                if line[:2] == ".I":
                    line = line.split(" ")
                    current_test_nb = int(line[1])
                    D[current_test_nb] = ""
            
            if current_section_list == ".W" and line[:2] !=".W":
                D[current_test_nb] += " " + line[:-1]
        return D

def calculate_average(D):
    """Method that takes all the interpolation of precision/recall for different queries. 
       It calculates the average for precision for each recall.
       It return a dictionnary with recall as key, and precision as value.
       """
    new_dic = {}
    nb_test_query = 0
    for dic in D:
        nb_test_query += 1
        for rappel in dic:
            if rappel in new_dic:
                new_dic[rappel] += dic[rappel]
            else:
                new_dic[rappel] = dic[rappel]
    
    for rappel in new_dic:
        new_dic[rappel] /= nb_test_query

    return new_dic 



def main(collection_path, stopwords_path):
    """Main Method that produces the interpolate curve Precision/Recall from the query set and the MAP"""

    #Creation of the CACM index
    index = IndexCACMMemory()
    index.parserCacm("CACM/cacm.all")
    index.parserCacm(collection_path)
    index.tokenizerCacm()
    index.manage_tokens_collectionCacm(stopwords_path)
    index.index_inverse()
    index.weight_calculation_index()

    #Get the queries under the dictionnary format from the file query.text file
    queries = loop_query_test()

    #List for recall precision interpolation
    L=[]
    #average precision list
    ap_list = []
    #E F measures list
    EF_list = []
    #R precision list
    R_list = []

    for query in queries:
        relevant_doc = get_doc_relevants_query(query)
        A = Evaluation(query = queries[query], sample_test=relevant_doc)
        A.precision_for_relevant_doc(index)
        A.interpolate_rappel_precision()
        L.append(A.rappel_precision_interpolation)
        #Computing average precision
        ap_list += [A.average_precision(index)]
        #Computes E, F measures
        EF_list += [A.compute_measures(index, 20)]
        #Computes R precision
        R_list += [A.rprecision(index)]

    #Calculate mean average precision
    map_v = mean(ap_list)
    print("The mean average precision is {}".format(str(map_v)))

    #Calculate the average of each value of recall
    interpolate_general = calculate_average(L)

    #Make the interpolate curve Rappel-Precision
    rappels = list(interpolate_general.keys())
    precisions = list(interpolate_general.values())
    plt.scatter(rappels, precisions)
    plt.title('Precision/Recall interpolation')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.show()
    
    #Print E,F,R measures for the queries
    for i in range(len(queries)):
        if EF_list[i][0] == None:
            print("Pour la requete {}: \n"
                  "Elle ne comporte pas de documents pertinents et nous ne pouvons donc calculer les statistiques\n".format(
                str(queries[i+1])
            ))
        else:
            print(
                "Pour la requête {0}:\n la E measure vaut {1}, la F measure vaut {2} et la R précision vaut {3}\n".format(
                    str(queries[i + 1]), str(EF_list[i][0]), EF_list[i][1], R_list[i]))

if __name__ == "__main__":
    print('CACM evaluation')
    collection_path = input("What is the path of the CACM collection ? ")
    stopwords_path = "CACM/common_words"
    main(collection_path,stopwords_path)
                





