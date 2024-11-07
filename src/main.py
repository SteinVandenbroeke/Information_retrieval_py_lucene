import sys, os, lucene
import datetime

from DocumentIndexing import DocumentIndexing
from DocumentRetrieval import DocumentRetrieval
from TestQueries import test_queries

start_time = datetime.datetime.now()
docIndexing = DocumentIndexing("index")
docIndexing.add_folder("../datasets/full_docs")
docIndexing.index_folders()
docIndexing.commit_and_close()
end_time = datetime.datetime.now()
print("Elapsed time: ", end_time-start_time)

docRetrieval = DocumentRetrieval("index")
# docRetrieval.search("insurance and cars and automobiles")
test_queries(docRetrieval, False)
end_time = datetime.datetime.now()
print("Elapsed time: ", end_time-start_time)