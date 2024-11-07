import os

import lucene
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.analysis.standard import StandardAnalyzer
from java.nio.file import Paths
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.document import TextField, Field
from org.apache.lucene.document import Document
from org.apache.lucene.index import IndexWriterConfig
from org.apache.lucene.index import IndexWriter
from org.apache.lucene.index import Term

lucene.initVM()
class DocumentIndexing:
    def __init__(self, index_location, analyzer = StandardAnalyzer()):
        self.folders = []
        self.analyzer = StandardAnalyzer()
        directory = FSDirectory.open(Paths.get(index_location))

        # Instantiate indexing and configure index writer
        indexWriterConfig = IndexWriterConfig(analyzer)
        #indexWriterConfig.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND) #OpenMode: APPEND, CREATE, CREATE_OR_APPEND
        self.indexWriter = IndexWriter(directory, indexWriterConfig)

    def add_folder(self, path):
        self.folders.append(path)

    def index_folders(self):
        for path in self.folders:
            for d in os.listdir(path):
                if d.endswith('.txt'):
                    file_path = os.path.join(path, d)
                    self.index_document(file_path)
            self.indexWriter.commit()

    def index_document(self, path):
        document = Document()
        f = open(path, "r")
        info = os.stat(path)
        #print("file info", info)
        file_name = f.name
        file_content = f.read()
        # add fields and field content to document
        # Field.Store.YES whether to store this field for retrieval
        document.add(TextField("text_content", file_content, Field.Store.YES))
        document.add(TextField("file_name", file_name, Field.Store.YES))
        document.add(TextField("file_path", path, Field.Store.YES))
        term = Term("file_path", path)
        self.indexWriter.updateDocument(term, document)




