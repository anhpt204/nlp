'''
Created on Jul 7, 2015

@author: pta
'''

import abc
import random, math, numpy, array
from os import listdir
from os.path import isfile, join


from document import helper
from deap import creator, tools, base
from tokenizer.ETokenizer import ETokenizer
from document.DUCDocument import DUC04Document
from document.DocumentCollection import DocumentCollection
from summarizer.optimizer import MDSDEOptimizer, MDSSaDEOptimizer
    
class MultiDocsSummarizer(object):
    '''
    classdocs
    '''
    __metaclass__ = abc.ABCMeta
    

    def __init__(self, max_size=250):
        '''
        Constructor
        '''
        self.multiDocs = None
        self.tokenizer = None
        self.optimizer = None

        self.max_size = max_size
    
    @abc.abstractmethod    
    def getTokenizer(self):
        pass
    
    @abc.abstractmethod
    def getDocumentCollection(self, document_collection_dir):
        pass
    
    @abc.abstractmethod
    def getOptimizer(self):
        pass
    
    @abc.abstractmethod
    def getIndexSelectedSentences(self):
        pass
    
    def renewMultiDocs(self, indexSelectedSentences):
        self.multiDocs = self.multiDocs.renewFromSummary(indexSelectedSentences)
        self.optimizer = self.getOptimizer()
        
                
    def summarize(self, document_collection_dir):
        self.tokenizer = self.getTokenizer()
        self.multiDocs = self.getDocumentCollection(document_collection_dir)    
        self.optimizer = self.getOptimizer()
        
        return self.optimizer.solve()
    

class DUCSummarizer(MultiDocsSummarizer):
    '''
    multi-document summarization for DUC Data
    '''
    def getTokenizer(self):
        return ETokenizer()
        
        
class DUC04DESummarizer(DUCSummarizer):
    '''
    DE algorithm for DUC 2007 dataset
    '''
    def getDocumentCollection(self, document_collection_dir):
        files = [join(document_collection_dir, file_name) for file_name in listdir(document_collection_dir)]
        files = [f for f in files if isfile(f)]
        
        if files == None or len(files) == 0:
            raise Exception('error in path to folder containing data')
        
        docCollection = []
        for file in files:
            doc = DUC04Document(self.tokenizer)
            doc.parseDocument(file)
            docCollection.append(doc)
        
        multiDocs = DocumentCollection()
        multiDocs.setDocuments(docCollection)
        
        return multiDocs
    
    def getIndexSelectedSentences(self):
        return [i for i in xrange(self.multiDocs.numOfSentences) if self.optimizer.best_so_far_b[i] == 1]
    
    def getOptimizer(self):
        return MDSDEOptimizer(self.multiDocs)

class DUC04SaDESummarizer(DUC04DESummarizer):
    '''
    Self-adaptive DE algorithm for DUC 2004 dataset
    '''
    def getOptimizer(self):
        return MDSSaDEOptimizer(self.multiDocs)

if __name__ == "__main__":
        
    text_dir = '/home/pta/projects/nlp/data/DUC2004/testdata/'
    out_dir = '/home/pta/projects/nlp/data/DUC2004/models/'
    
    problems = listdir(text_dir)
    
    for problem in problems:
        print problem
        doc_folder = join(text_dir, problem)

        ducSummarizer = DUC04DESummarizer()       
#     ducSummarizer = DUC04SaDESummarizer()
        
        summary = ducSummarizer.summarize(doc_folder)

        out_file = join(out_dir, problem + ".DE")
        open(out_file, 'w').write(summary)

    
    
