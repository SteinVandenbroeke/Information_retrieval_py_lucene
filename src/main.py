import sys, os, lucene
import datetime

from DocumentIndexing import DocumentIndexing
from DocumentRetrieval import DocumentRetrieval
from TestQueries import test_queries

from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import StopAnalyzer
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.search.similarities import ClassicSimilarity
from src.CustomImplementations.CustomAnalyzer import CustomStemmingAnalyzer
from org.apache.lucene.search.similarities import LMJelinekMercerSimilarity
from org.apache.lucene.search.similarities import LMDirichletSimilarity

def testRun(analyzer, dataset, retrival_model, query_parser, scoring_model):
    print(str(analyzer.__name__))
    start_time = datetime.datetime.now()
    doc_index_StandardAnalyzer = DocumentIndexing(str(analyzer.__name__), analyzer())
    doc_index_StandardAnalyzer.add_folder(dataset, True)
    doc_index_StandardAnalyzer.index_folders()
    docRetrieval = DocumentRetrieval(str(analyzer.__name__), analyzer(), retrival_model)
    passes_failes = test_queries(docRetrieval, True)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print("run time:", elapsed_time)
    doc_index_StandardAnalyzer.close()
    return (elapsed_time, passes_failes)


def analyserTest(data_set):
    analyserTest_start_time = datetime.datetime.now()
    results = []
    results.append(("StandardAnalyzer", testRun(StandardAnalyzer, data_set, ClassicSimilarity(), None, None)))
    results.append(("SimpleAnalyzer", testRun(SimpleAnalyzer, data_set, ClassicSimilarity(), None, None)))
    results.append(("WhitespaceAnalyzer", testRun(WhitespaceAnalyzer, data_set, ClassicSimilarity(), None, None)))
    results.append(("EnglishAnalyzer", testRun(EnglishAnalyzer, data_set, ClassicSimilarity(), None, None)))
    #results.append(testRun(CustomStemmingAnalyzer, data_set, ClassicSimilarity(), None, None))TODO
    analyserTest_end_time = datetime.datetime.now()
    print("Analyser test time: ", analyserTest_end_time - analyserTest_start_time)
    return results

def retrivalModelTest(data_set):
    retrivalModel_start_time = datetime.datetime.now()
    results = []
    results.append(("ClassicSimilarity", testRun(StandardAnalyzer, data_set, ClassicSimilarity(), None, None)))
    results.append(("BM25Similarity", testRun(StandardAnalyzer, data_set, BM25Similarity(), None, None)))
    results.append(("LMDirichletSimilarity", testRun(StandardAnalyzer, data_set, LMDirichletSimilarity(), None, None)))
    results.append(("LMJelinekMercerSimilarity(0.7)", testRun(StandardAnalyzer, data_set, LMJelinekMercerSimilarity(0.7), None, None)))
    results.append(("LMJelinekMercerSimilarity(0.5)", testRun(StandardAnalyzer, data_set, LMJelinekMercerSimilarity(0.5), None, None)))
    results.append(("LMJelinekMercerSimilarity(0.9)", testRun(StandardAnalyzer, data_set, LMJelinekMercerSimilarity(0.9), None, None)))
    retrivalModel_end_time = datetime.datetime.now()
    print("Retrivalmodel test time: ", retrivalModel_end_time - retrivalModel_start_time)
    return results

# docIndexing.add_folder("../datasets/

start_time = datetime.datetime.now()
analyserResults = analyserTest("../datasets/full_docs_small")
retrivalResults = retrivalModelTest("../datasets/full_docs_small")
print("anyser results", analyserResults)
print("model retrive resulte", retrivalResults)
end_time = datetime.datetime.now()
print("Total run time: ", end_time - start_time)