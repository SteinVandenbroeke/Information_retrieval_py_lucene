import lucene
from org.apache.lucene.index import DirectoryReader
from java.nio.file import Paths

class DocumentIndexing:
    def __init__(self):
        self.folders = []

    def addFolder(self, path):
        self.folders.append(path)

    def indexFolders(self):
        for item in self.folders:
            index_dir = FSDirectory.open(Paths.get(index_path))
