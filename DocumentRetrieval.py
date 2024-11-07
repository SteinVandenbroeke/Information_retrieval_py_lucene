import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from java.nio.file import Paths
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.document import TextField, Field
from org.apache.lucene.document import Document
from org.apache.lucene.index import IndexWriterConfig
from org.apache.lucene.index import IndexWriter
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser

class DocumentRetrieval:
    def __init__(self, index_location, analyzer = StandardAnalyzer()):
        directory = FSDirectory.open(Paths.get(index_location))
        reader = DirectoryReader.open(directory)
        self.searcher = IndexSearcher(reader)
        self.query_parser = QueryParser("text_content", analyzer)

    def search(self, querystring):
        query = self.query_parser.parse(querystring)

        for hit in self.searcher.search(query, 10).scoreDocs.search(query):
            doc_id = hit.doc
            doc = self.get_doc(doc_id)
            print(f"Found document with content: {doc.get('text_content')}")
            print(f"Path: {doc.get('file_path')}")
            print(f"Score: {hit.score}")
            print()
            print()

    def get_doc(self, doc_id):
        return self.searcher.doc(doc_id)