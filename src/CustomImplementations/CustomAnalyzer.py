import lucene
from org.apache.lucene.analysis.standard import StandardTokenizer
from org.apache.lucene.analysis.core import LowerCaseFilter
from org.apache.lucene.analysis.en import PorterStemFilter
from org.apache.lucene.analysis import Analyzer, TokenStream
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from java.io import StringReader

class CustomStemmingAnalyzer(Analyzer):
    def createComponents(self, fieldName):
        # Tokenizer: standard tokenizer splits text on word boundaries
        tokenizer = StandardTokenizer()
        # TokenStreamComponents: Apply filters in sequence
        # 1. LowerCaseFilter to normalize case
        # 2. PorterStemFilter to apply stemming
        tokenStream = LowerCaseFilter(tokenizer)
        tokenStream = PorterStemFilter(tokenStream)
        return Analyzer.TokenStreamComponents(tokenizer, tokenStream)