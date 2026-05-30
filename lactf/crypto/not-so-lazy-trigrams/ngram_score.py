# Download and create English trigram statistics
from collections import defaultdict
import math

# Built-in common English trigrams with log probabilities
trigrams = {
    'the': -2.00, 'and': -2.92, 'ing': -2.93, 'ion': -3.47, 'tio': -3.76,
    'ent': -3.47, 'ati': -3.62, 'for': -3.76, 'her': -3.79, 'ter': -3.87,
    'hat': -3.91, 'tha': -3.91, 'ere': -3.98, 'ate': -4.06, 'his': -4.15,
    'con': -4.24, 'res': -4.30, 'ver': -4.40, 'all': -4.40, 'ons': -4.44,
    'nce': -4.44, 'nte': -4.44, 'men': -4.44, 'int': -4.50, 'est': -4.50,
}

class NGramScore:
    def __init__(self):
        self.ngrams = trigrams
        self.floor = -10.0
    
    def score(self, text):
        score = 0.0
        for i in range(len(text) - 2):
            trigram = text[i:i+3]
            score += self.ngrams.get(trigram, self.floor)
        return score

if __name__ == '__main__':
    scorer = NGramScore()
    print(scorer.score('the quick brown fox'))
    print(scorer.score('xyz qwerty asdf'))
