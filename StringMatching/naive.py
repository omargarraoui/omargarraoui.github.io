class NaiveMatcher:
    """
    Algoritmo di ricerca Naive/Brute Force.
    Controlla ogni posizione del testo una per una.
    """
    def __init__(self, pattern):
        self.pattern = pattern
        self.m = len(pattern)
        self.comparisons = 0
    
    def search(self, text):
        """
        Cerca il pattern nel testo.
        Ritorna: indice della prima occorrenza o -1 se non trovato
        """
        self.comparisons = 0
        n = len(text)
        
        for i in range(n - self.m + 1):
            j = 0
            while j < self.m:
                self.comparisons += 1
                if text[i + j] != self.pattern[j]:
                    break
                j += 1
            if j == self.m:
                return i
        return -1
    
    def get_comparisons(self):
        return self.comparisons