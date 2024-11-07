import sys, os, lucene

from string import Template
from datetime import datetime
from getopt import getopt, GetoptError
from org.apache.lucene.search import TermQuery
from org.apache.lucene.index import Term
from org.apache.lucene.queryparser.classic import QueryParser

from DocumentIndexing import DocumentIndexing
from DocumentRetrieval import DocumentRetrieval


def main():
    docIndexing = DocumentIndexing("index")
    docIndexing.add_folder("../datasets/full_docs_small")
    docIndexing.index_folders()
    docIndexing.indexWriter.close()
    docRetrieval = DocumentRetrieval("index")
    docRetrieval.search("insurance")

print(lucene.VERSION)

if __name__ == '__main__':
    main()
