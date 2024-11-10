from org.apache.lucene.analysis import Analyzer
from org.apache.lucene.analysis.standard import StandardTokenizer
from org.apache.lucene.analysis.core import LowerCaseFilter
from org.apache.lucene.analysis.standard import StopFilter
from org.apache.lucene.analysis.util import CharArraySet
from org.apache.lucene.util import Version

class CustomAnalyzer(Analyzer):
    def __init__(self):
        super().__init__()

    def createComponents(self):
        # Create the tokenizer (StandardTokenizer)
        tokenizer = StandardTokenizer()

        # Apply the lowercase filter
        tokenStream = LowerCaseFilter(tokenizer)

        # Define stopwords
        stopWords = CharArraySet.stopWordsSet()  # This gives you a default set of English stopwords
        # Apply stopword filter
        tokenStream = StopFilter(tokenStream, stopWords)

        # Return the components (tokenizer + token stream with filters)
        return Analyzer.TokenStreamComponents(tokenizer, tokenStream)