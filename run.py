'''
Created on Jul 17, 2015

@author: pta
'''
from os import listdir
from os.path import join
from summarizer.multiDocs import DUC04DESummarizer, DUC04SaDESummarizer
from summarizer.multiStepOptimizer import MultiStepOptimizer


text_dir = 'data/DUC2004/testdata/'
out_dir = 'data/DUC2004/models/'
    
problems = listdir(text_dir)

def oneStepOptimizing():
    
    
    for problem in problems[:5]:
        print problem
        doc_folder = join(text_dir, problem)

#         ducSummarizer = DUC04DESummarizer()       
        ducSummarizer = DUC04SaDESummarizer()
        
        summary = ducSummarizer.summarize(doc_folder)

        out_file = join(out_dir, problem + ".SaDE")
        open(out_file, 'w').write(summary)
        
def multiStepOptimizing():
    for problem in problems:
        doc_folder = join(text_dir, problem)

        optimizer = MultiStepOptimizer()
        
        # summarizer
        ducSummarizer = DUC04DESummarizer()       
#         ducSummarizer = DUC04SaDESummarizer()

        summary = optimizer.solve(ducSummarizer, doc_folder)
        
        out_file = join(out_dir, problem + ".MulDE")
        open(out_file, 'w').write(summary)
    
if __name__ == '__main__':
    
    oneStepOptimizing()
    
#     multiStepOptimizing()
    
