import os
from datetime import datetime

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
import json

lucene.initVM()
class DocumentIndexing:
    def __init__(self, index_location, analyzer = StandardAnalyzer()):
        self.folders = {}
        if not os.path.isdir(index_location):
            os.makedirs(index_location)
        if os.path.isfile(index_location + "/indexed_folders.json"):
            with open(index_location + "/indexed_folders.json", 'r') as openfile:
                # Reading from json file
                self.folders = json.load(openfile)


        self.analyzer = analyzer
        self.index_location = index_location
        directory = FSDirectory.open(Paths.get(index_location))

        # Instantiate indexing and configure index writer
        indexWriterConfig = IndexWriterConfig(self.analyzer)
        indexWriterConfig.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND) #OpenMode: APPEND, CREATE, CREATE_OR_APPEND
        self.indexWriter = IndexWriter(directory, indexWriterConfig)

    def add_folder(self, path, reindex = False):
        if path not in self.folders or reindex:
            self.folders[path] = None

    def index_folders(self, reindex = False, expireTime = None):
        start_time = datetime.now()
        for path, lastUpdate in self.folders.items():
            lastUpdate_dt = datetime.fromtimestamp(lastUpdate) if lastUpdate is not None else None
            if lastUpdate is None or reindex or (expireTime is not None and lastUpdate_dt + expireTime < datetime.now()):
                print("indexing path: ", path)
                for d in os.listdir(path):
                    if d.endswith('.txt'):
                        file_path = os.path.join(path, d)
                        self.index_document(file_path)
                self.indexWriter.commit()
                unix_timestamp = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
                self.folders[path] = unix_timestamp
        end_time_query_test = datetime.now()
        print("Indexing time: ", end_time_query_test - start_time)


    def close(self):
        self.indexWriter.close()
        self.update_index_state()

    def index_document(self, path):
        document = Document()
        with open(path, "r") as f:
            file_content = f.read()
            file_name = os.path.basename(path)

        document.add(TextField("text_content", file_content, StringField.Store.NO))
        document.add(StringField("file_name", file_name, StringField.Store.YES))
        document.add(StringField("file_path", path, StringField.Store.YES))
        term = Term("file_path", path)
        self.indexWriter.updateDocument(term, document)

    def update_index_state(self):
        print(self.folders)
        json_object = json.dumps(self.folders, indent=4)
        # Writing to sample.json
        with open(self.index_location + "/indexed_folders.json", "w") as outfile:
            outfile.write(json_object)