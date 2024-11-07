import sys, os, lucene

from DocumentIndexing import DocumentIndexing
from DocumentRetrieval import DocumentRetrieval


docIndexing = DocumentIndexing("index")
docIndexing.add_folder("../datasets/full_docs_small")
docIndexing.index_folders()
docIndexing.commit_and_close()
docRetrieval = DocumentRetrieval("index")
docRetrieval.search("insurance and cars and automobiles")