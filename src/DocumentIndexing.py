import os

import lucene
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.analysis.standard import StandardAnalyzer
from java.nio.file import Paths
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.document import TextField, Field, StringField
from org.apache.lucene.document import Document
from org.apache.lucene.index import IndexWriterConfig
from org.apache.lucene.index import IndexWriter
from org.apache.lucene.index import Term

lucene.initVM()
class DocumentIndexing:
    def __init__(self, index_location, analyzer = StandardAnalyzer()):
        self.folders = []
        self.analyzer = analyzer
        directory = FSDirectory.open(Paths.get(index_location))

        # Instantiate indexing and configure index writer
        indexWriterConfig = IndexWriterConfig(self.analyzer)
        indexWriterConfig.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND) #OpenMode: APPEND, CREATE, CREATE_OR_APPEND
        self.indexWriter = IndexWriter(directory, indexWriterConfig)

    def add_folder(self, path):
        self.folders.append(path)

    def index_folders(self):
        for path in self.folders:
            for d in os.listdir(path):
                if d.endswith('.txt'):
                    file_path = os.path.join(path, d)
                    self.index_document(file_path)

    def commit_and_close(self):
        self.indexWriter.commit()
        self.indexWriter.close()

    def index_document(self, path):
        document = Document()
        with open(path, "r") as f:
            file_content = f.read()
            file_name = os.path.basename(path)

        document.add(TextField("text_content", file_content, StringField.Store.YES))
        document.add(StringField("file_name", file_name, StringField.Store.YES))
        document.add(StringField("file_path", path, StringField.Store.YES))
        term = Term("file_path", path)
        self.indexWriter.updateDocument(term, document)