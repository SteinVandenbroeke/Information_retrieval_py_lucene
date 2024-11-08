import datetime
import os

from DocumentRetrieval import DocumentRetrieval

import pandas as pd


def test_queries(docRetrieval, small = True):
    print("Testing queries for ", "small" if small else "big", " database:")
    query_path = "queries/dev_queries" + ("_small.csv" if small else ".csv")
    query_data = pd.read_csv(query_path, names=["Query number","Query"], skiprows=1)
    query_result_path = "queries/dev_query_results" + ("_small.csv" if small else ".csv")
    query_result_data = pd.read_csv(query_result_path, names=["Query_number","doc_number"], skiprows=1)

    passes = 0
    fails = 0

    for q in query_data.values:
        query_id = q[0]
        query = q[1]
        result = []
        for i in docRetrieval.search(query):
            doc_id = i.doc
            doc = docRetrieval.get_doc(doc_id)
            result.append(int(doc.get('file_name').replace("output_","").replace(".txt","")))

        query_result_doc = query_result_data[query_result_data['Query_number'] == query_id]['doc_number'].tolist()[0]

        if query_result_doc in result:
            passes += 1
            #print("passed")
        else:
            fails += 1
            #print("failed")
    print(passes, " out of ", passes+fails, " queries passed.")

# def create_result_csv(docsearch, small = True):
#     start_time = datetime.datetime.now()
#
#     print("Testing queries for ", "small" if small else "big", " database:")
#     query_path = "../queries/queries_test_set.csv"
#     query_data = pd.read_csv(query_path, names=["Query number","Query"], skiprows=1, delimiter='\t')
#
#     passes = 0
#     fails = 0
#     if os.path.isfile("../results/result.csv"):
#         os.remove("../results/result.csv")
#     with open('../results/result.csv', 'w') as file:
#         file.write(f"Query_number,doc_number\n")
#         for q in query_data.values:
#             query_id = q[0]
#             query = q[1]
#             results = docsearch.retrieve_documents(query, 10)
#             for result in results:
#                 file.write(f"{int(query_id)},{int(result)}\n")
#     end_time_query_test = datetime.datetime.now()
#     print("test csv time: ", end_time_query_test - start_time)
#
#
# def evaluation(docsearch, small=True):
#     start_time = datetime.datetime.now()
#
#     print("Testing queries for ", "small" if small else "big", " database:")
#     query_path = "../queries/dev_queries" + ("_small.csv" if small else ".csv")
#     query_data = pd.read_csv(query_path, names=["Query number", "Query"], skiprows=1)
#     query_result_path = "../queries/dev_query_results" + ("_small.csv" if small else ".csv")
#     query_result_data = pd.read_csv(query_result_path, names=["Query_number", "doc_number"], skiprows=1)
#
#     sumedP10 = 0.0
#     sumedR10 = 0.0
#     sumedP3 = 0.0
#     sumedR3 = 0.0
#     total = 0
#     for q in query_data.values:
#         query_id = q[0]
#         query = q[1]
#         results = docsearch.retrieve_documents(query, 10)
#
#         query_result_doc = query_result_data[query_result_data['Query_number'] == query_id]['doc_number'].tolist()
#         #print("Result doc", 10, query_id, query_result_doc, results)
#         r = len(list(set(results).intersection(set(query_result_doc))))
#             #print(results, query_result_doc, r, f"MAP@10: {r/1} MAR@10: {r/len(query_result_doc)}")
#         sumedP10 += r/10
#         sumedR10 += r/len(query_result_doc)
#
#         results = results[0:3]
#         #print("Result doc", 3, query_id, query_result_doc, results)
#         r = len(list(set(results).intersection(set(query_result_doc))))
#         sumedP3 += r / 3
#         sumedR3 += r/len(query_result_doc)
#
#         total += 1
#         if total % 100 == 0:
#             print("done evaluating: ", total)
#
#     end_time_query_test = datetime.datetime.now()
#     print("Query time: ", end_time_query_test - start_time)
#     print(f"MAP@3: {sumedP3/total} MAR@3: {sumedR3/total}")
#     print(f"MAP@10: {sumedP10 / total} MAR@10: {sumedR10 / total}")
#
