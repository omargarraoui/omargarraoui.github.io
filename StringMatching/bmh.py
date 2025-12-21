# ============================================================================
# FILE: bmh.py
# Algoritmo Boyer-Moore-Horspool (BMH) per Pattern Matching
# ============================================================================

class BMHMatcher:
    """
    Algoritmo Boyer-Moore-Horspool (BMH).
    Usa la Bad Character Heuristic per saltare porzioni del testo.
    Gold standard per la ricerca di pattern, combina semplicità e velocità.
    """
    def __init__(self, pattern):
        self.pattern = pattern
        self.m = len(pattern)
        self.shift_table = {}
        self.comparisons = 0
        
        # Pre-processing: costruisce la tabella di shift
        for i in range(self.m - 1):
            self.shift_table[pattern[i]] = self.m - 1 - i
    
    def search(self, text):
        """
        Cerca il pattern nel testo usando BMH.
        Ritorna: indice della prima occorrenza o -1 se non trovato
        """
        self.comparisons = 0
        n = len(text)
        i = 0
        
        while i <= n - self.m:
            # Confronta da destra verso sinistra
            j = self.m - 1
            
            while j >= 0:
                self.comparisons += 1
                if text[i + j] != self.pattern[j]:
                    break
                j -= 1
            
            if j < 0:
                return i  # Match trovato
            
            # Calcola il salto usando Bad Character Heuristic
            char = text[i + self.m - 1] if i + self.m - 1 < n else None
            if char in self.shift_table:
                i += self.shift_table[char]
            else:
                i += self.m
        
        return -1
    
    def get_comparisons(self):
        return self.comparisons