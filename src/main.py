import sys, os, lucene
import datetime

from DocumentIndexing import DocumentIndexing
from DocumentRetrieval import DocumentRetrieval
from TestQueries import test_queries, create_result_csv, evaluation

from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import StopAnalyzer
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.search.similarities import ClassicSimilarity
from org.apache.lucene.search.similarities import LMJelinekMercerSimilarity
from org.apache.lucene.search.similarities import LMDirichletSimilarity
import matplotlib.pyplot as plt
import numpy as np


def plot(data, plot_metrics, as_titles = ["x-as", "y-as"], title= "Plot"):
    # Extracting analyzer names, metrics, and values
    analyzer_names = [list(d.keys())[0] for d in data]
    metrics = list(data[0][analyzer_names[0]][1].keys())
    values = {metric: [
        d[analyzer][1][metric] if isinstance(d[analyzer][1][metric], float) else d[analyzer][1][metric].total_seconds()
        for d in data for analyzer in d] for metric in metrics}

    # Plotting the bar chart
    bar_width = 0.10
    x = np.arange(len(analyzer_names))

    plt.figure(figsize=(22, 8))
    for i, metric in enumerate(metrics):
        if metric not in plot_metrics:
            continue
        plt.bar(x + i * bar_width, values[metric], bar_width, label=metric)

    # Labeling and legend
    plt.xlabel(as_titles[0])
    plt.ylabel(as_titles[1])
    plt.title(title)
    plt.xticks(x + bar_width * (len(plot_metrics) - 1) / 2, analyzer_names)
    plt.legend(title="Metrics")
    plt.tight_layout()

    plt.show()

def testRun(analyzer, dataset, retrival_model, query_parser, scoring_model):
    small = False
    if "small" in dataset:
        small = True

    print(str(analyzer.__name__) + " and " + str(retrival_model) + ":")
    start_time = datetime.datetime.now()
    doc_index_StandardAnalyzer = DocumentIndexing(str(dataset.split("/").pop() + str(analyzer.__name__)), analyzer())
    doc_index_StandardAnalyzer.add_folder(dataset, True)
    doc_index_StandardAnalyzer.index_folders()
    docRetrieval = DocumentRetrieval(str(dataset.split("/").pop() + str(analyzer.__name__)), analyzer(), retrival_model)
    passes_failes = evaluation(docRetrieval, small)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print("run time:", elapsed_time)
    doc_index_StandardAnalyzer.close()
    print("-----------------------------------------------")
    return (elapsed_time, passes_failes)


def analyserTest(data_set, to_test = ["StandardAnalyzer", "SimpleAnalyzer", "WhitespaceAnalyzer", "EnglishAnalyzer"]):
    analyserTest_start_time = datetime.datetime.now()
    results = []
    if "StandardAnalyzer" in to_test:
        results.append({"StandardAnalyzer and ClassicSimilarity": testRun(StandardAnalyzer, data_set, ClassicSimilarity(), None, None)})

    if "SimpleAnalyzer" in to_test:
        results.append({"SimpleAnalyzer and ClassicSimilarity": testRun(SimpleAnalyzer, data_set, ClassicSimilarity(), None, None)})

    if "WhitespaceAnalyzer" in to_test:
        results.append({"WhitespaceAnalyzer and ClassicSimilarity": testRun(WhitespaceAnalyzer, data_set, ClassicSimilarity(), None, None)})

    if "EnglishAnalyzer" in to_test:
        results.append({"EnglishAnalyzer and ClassicSimilarity": testRun(EnglishAnalyzer, data_set, ClassicSimilarity(), None, None)})
    #results.append(testRun(CustomStemmingAnalyzer, data_set, ClassicSimilarity(), None, None))TODO
    analyserTest_end_time = datetime.datetime.now()
    print("Analyser test time: ", analyserTest_end_time - analyserTest_start_time)
    return results

def retrivalModelTest(data_set, to_test = ["ClassicSimilarity", "BM25Similarity", "LMDirichletSimilarity", "LMJelinekMercerSimilarity(0.7)", "LMJelinekMercerSimilarity(0.5)", "LMJelinekMercerSimilarity(0.9)"]):
    retrivalModel_start_time = datetime.datetime.now()
    results = []
    if "ClassicSimilarity" in to_test:
        results.append({"StandardAnalyzer and ClassicSimilarity": testRun(StandardAnalyzer, data_set, ClassicSimilarity(), None, None)})

    if "BM25Similarity" in to_test:
        results.append({"StandardAnalyzer and BM25Similarity": testRun(StandardAnalyzer, data_set, BM25Similarity(), None, None)})

    if "LMDirichletSimilarity" in to_test:
        results.append({"StandardAnalyzer and LMDirichletSimilarity": testRun(StandardAnalyzer, data_set, LMDirichletSimilarity(), None, None)})

    if "LMJelinekMercerSimilarity(0.7)" in to_test:
        results.append({"StandardAnalyzer and LMJelinekMercerSimilarity(0.7)": testRun(StandardAnalyzer, data_set, LMJelinekMercerSimilarity(0.7), None, None)})

    if "LMJelinekMercerSimilarity(0.5)" in to_test:
        results.append({"StandardAnalyzer and LMJelinekMercerSimilarity(0.5)": testRun(StandardAnalyzer, data_set, LMJelinekMercerSimilarity(0.5), None, None)})

    if "LMJelinekMercerSimilarity(0.9)" in to_test:
        results.append({"StandardAnalyzer and LMJelinekMercerSimilarity(0.9)": testRun(StandardAnalyzer, data_set, LMJelinekMercerSimilarity(0.9), None, None)})
    retrivalModel_end_time = datetime.datetime.now()
    print("Retrivalmodel test time: ", retrivalModel_end_time - retrivalModel_start_time)
    return results


# docIndexing.add_folder("../datasets/

start_time = datetime.datetime.now()
# analyserResults = analyserTest("../datasets/full_docs_small")
# retrivalResults = retrivalModelTest("../datasets/full_docs_small")
# print("anyser results", analyserResults)
# print("model retrive resulte", retrivalResults)
#
#
# plot(analyserResults, ["MAP@1", "MAP@3", "MAP@5", "MAP@10"], ["Analysers", "MAP@K"], "Analysers precision small dataset")
# plot(analyserResults, ["MAR@1", "MAR@3", "MAR@5", "MAR@10"], ["Analysers", "MAR@K"], "Analysers retrival small dataset")
# plot(analyserResults, ["QueryTime"], ["Analysers", "Time"])
#
# plot(retrivalResults, ["MAP@1", "MAP@3", "MAP@5", "MAP@10"], ["Retrival models", "MAP@K"], "Retrival models precision small dataset")
# plot(retrivalResults, ["MAR@1", "MAR@3", "MAR@5", "MAR@10"], ["Retrival models", "MAR@K"], "Retrival models precision small dataset")
# plot(retrivalResults, ["QueryTime"], ["Retrival models", "Time"], "Retrival models run time small dataset")
#


print("---------- Large dataset ----------")
analyserResults = analyserTest("../datasets/full_docs", ["StandardAnalyzer", "EnglishAnalyzer"])
analyserResults.append({"StandardAnalyzer and LMDirichletSimilarity": testRun(StandardAnalyzer, "../datasets/full_docs", LMDirichletSimilarity(), None, None)})
analyserResults.append({"EnglihAnalyzer and LMDirichletSimilarity": testRun(EnglishAnalyzer, "../datasets/full_docs", LMDirichletSimilarity(), None, None)})
print("Large dataset results", analyserResults)

plot(analyserResults, ["MAP@1", "MAP@3", "MAP@5", "MAP@10"], ["Analysers", "MAP@K"], "Large dataset results MAP@K")
plot(analyserResults, ["MAR@1", "MAR@3", "MAR@5", "MAR@10"], ["Analysers", "MAR@K"], "Large dataset results MAP@R")
plot(analyserResults, ["QueryTime"], ["Analysers", "Time"])

end_time = datetime.datetime.now()
print("Total run time: ", end_time - start_time)
