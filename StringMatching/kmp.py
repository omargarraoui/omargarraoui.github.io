# ============================================================================
# FILE: kmp.py
# Algoritmo Knuth-Morris-Pratt (KMP) per Pattern Matching
# ============================================================================

class KMPMatcher:
    """
    Algoritmo KMP (Knuth-Morris-Pratt).
    Non torna mai indietro nel testo, usa una tabella LPS (Longest Proper Prefix).
    Ottimo per testi ripetitivi o alfabeti piccoli.
    """
    def __init__(self, pattern):
        self.pattern = pattern
        self.m = len(pattern)
        self.lps = self._compute_lps()
        self.comparisons = 0
    
    def _compute_lps(self):
        """
        Calcola la tabella LPS (Longest Proper Prefix which is also Suffix).
        Usata per evitare confronti ridondanti.
        """
        lps = [0] * self.m
        length = 0
        i = 1
        
        while i < self.m:
            if self.pattern[i] == self.pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    def search(self, text):
        """
        Cerca il pattern nel testo usando KMP.
        Ritorna: indice della prima occorrenza o -1 se non trovato
        """
        self.comparisons = 0
        n = len(text)
        i = 0  # indice per text
        j = 0  # indice per pattern
        
        while i < n:
            self.comparisons += 1
            if self.pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == self.m:
                return i - j
            elif i < n and self.pattern[j] != text[i]:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
        return -1
    
    def get_comparisons(self):
        return self.comparisons