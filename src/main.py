import sys, os, lucene
import datetime

from DocumentIndexing import DocumentIndexing
from DocumentRetrieval import DocumentRetrieval
from TestQueries import test_queries, create_result_csv, evaluation

from org.apache.lucene.analysis.en import EnglishAnalyzer


start_time = datetime.datetime.now()
docIndexing = DocumentIndexing("index",  EnglishAnalyzer())

# docIndexing.add_folder("../datasets/full_docs")
docIndexing.add_folder("../datasets/full_docs_small")
# docIndexing.add_folder("../datasets/full_docs_test", True)

docIndexing.index_folders() # False, datetime.timedelta(seconds=20)
docIndexing.close()
end_time = datetime.datetime.now()
print("Elapsed time: ", end_time-start_time)

docRetrieval = DocumentRetrieval("index", EnglishAnalyzer())
test_queries(docRetrieval, True)
# end_time = datetime.datetime.now()
# print(docRetrieval.search("test",2))
evaluation(docRetrieval, True)