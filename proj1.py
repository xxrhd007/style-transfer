import re
import sys

from math  import log10
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env



class proj1(MRJob):
    def mapper(self, _, line):
        year = line[:4]
        words = line[9:]

        words = re.split(" ", words.lower())

        for word in words:
            if(len(word))!=0:
                yield word + "," + str(year), 1
                yield word + ",*", 1

    def combiner(self, key, values):
        yield (key), sum(values)

    def reducer_init(self):
        self.marginal = {}
        
        
    def reducer(self, key, count):
        w1, w2 = key.split(",", 1)
        if w2 == "*":
            if w1 in self.marginal:
                self.marginal[w1]+=1
            else:
                self.marginal[w1]=1
                
        else:
            counts = sum(count)
            yield w1, (w2, counts)
            


    def TF_IDF(self, word, year_count):
        num = 0
        year = []
        freq = []
        for f in year_count:
            year.append(f[0])
            freq.append(f[1])
            num += 1

        IDF = log10(int(N) / num)
        
        for i in range(len(year)):
            tfidf=IDF*freq[i]
            if tfidf>int(beta):
                yield word,year[i]+','+str(tfidf)
                
    def reduce_sort1(self, key, values):
        yield None, (key,values)

    def reduce_sort(self, _, values):
        for key, value in sorted(values):
            yield key,value
    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                combiner=self.combiner,
                reducer_init=self.reducer_init,
                reducer=self.reducer
            ),
            MRStep(
                reducer=self.TF_IDF
            ),
            MRStep(
                mapper=self.reduce_sort1,
                reducer=self.reduce_sort
            )
        ]
    SORT_VALUES = True
            
    JOBCONF = {
        #'mapreduce.map.output.key.field.separator':',',
        'mapreduce.job.reduces':2,
        #'mapreduce.partition.keypartitioner.options':'-k1,1'
    }
    N = jobconf_from_env('myjob.settings.years'),
    beta =jobconf_from_env('myjob.settings.beta')
if __name__ == '__main__':
    proj1.run()
