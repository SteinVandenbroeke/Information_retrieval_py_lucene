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
from org.apache.lucene.queryparser.classic import QueryParserBase


class DocumentRetrieval:
    def __init__(self, index_location, analyzer = StandardAnalyzer()):
        directory = FSDirectory.open(Paths.get(index_location))
        reader = DirectoryReader.open(directory)
        self.searcher = IndexSearcher(reader)
        self.query_parser = QueryParser("text_content", analyzer)

    def search(self, querystring, result_amount):
        escaped_querystring = QueryParserBase.escape(querystring)
        query = self.query_parser.parse(escaped_querystring)
        hits = self.searcher.search(query, result_amount).scoreDocs
        return hits

    def get_doc(self, doc_id):
        return self.searcher.doc(doc_id)
