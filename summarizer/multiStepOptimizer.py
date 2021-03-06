'''
Created on Jul 13, 2015

@author: pta
'''
from summarizer.multiDocs import DUC04SaDESummarizer
class MultiStepOptimizer(object):
    '''
    classdocs
    '''


#     def __init__(self, optimizer, summarizer):
#         '''
#         Constructor
#         '''
#         self.optimizer = optimizer
#         self.summarizer = summarizer
        
    def solve(self, summarizer, path_to_data_folder):
        summarizer.summarize(path_to_data_folder)
        
        summary_size = summarizer.optimizer.getNumOfTerms(summarizer.optimizer.best_so_far_b)
        summary_text = ''
        while summary_size > summarizer.max_size:
            indexSelectedSentences = summarizer.getIndexSelectedSentences()
            summarizer.renewMultiDocs(indexSelectedSentences)
            summary_text = summarizer.optimizer.solve()
            summary_size = summarizer.optimizer.getNumOfTerms(summarizer.optimizer.best_so_far_b)
            
        return summary_text
    
if __name__ == "__main__":
        
    text_dir = '/home/pta/projects/nlp/data/DUC2004/testdata/d31043t/'
    optimizer = MultiStepOptimizer()
#     ducSummarizer = DUC04DESummarizer()       
    ducSummarizer = DUC04SaDESummarizer()
#     ducSummarizer.summarize(text_dir)
    optimizer.solve(ducSummarizer, text_dir)
            