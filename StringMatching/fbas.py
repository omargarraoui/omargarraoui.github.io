# ============================================================================
# FILE: fbas.py
# Algoritmo FBAS (Frequency-Based Anchor Search) per Pattern Matching
# ============================================================================

class FBASMatcher:
    """
    Algoritmo FBAS (Frequency-Based Anchor Search).
    Innovazione chiave: sceglie come "ancora" il carattere più raro nel pattern
    (basandosi su frequenze statistiche) e lo controlla per primo.
    Combina analisi statistica con Bad Character Heuristic di BMH.
    """
    def __init__(self, pattern):
        self.pattern = pattern
        self.m = len(pattern)
        self.comparisons = 0
        
        if self.m == 0:
            raise ValueError("Pattern vuoto")
        
        # Tabella frequenze (più basso = più raro)
        # Basata su frequenze standard italiano/inglese
        self.freq_table = {
            'z': 1, 'j': 2, 'x': 3, 'q': 4, 'k': 5,
            'b': 10, 'g': 11, 'h': 12, 'y': 13, 'p': 14,
            'm': 15, 'u': 16, 'c': 17, 'l': 18, 'd': 19,
            'r': 20, 'w': 21, 'f': 22, 's': 23, 'n': 24,
            't': 25, 'i': 26, 'o': 27, 'a': 28, 'e': 29
        }
        
        # INNOVAZIONE: Trova l'ancora (carattere più raro nel pattern)
        self.anchor_idx = 0
        min_freq = 1000
        for i, char in enumerate(pattern):
            score = self.freq_table.get(char.lower(), 50)
            if score < min_freq:
                min_freq = score
                self.anchor_idx = i
        
        self.anchor_char = pattern[self.anchor_idx]
        
        # Pre-processing: Bad Character Heuristic (come BMH)
        self.shift_table = {}
        for i in range(self.m - 1):
            self.shift_table[pattern[i]] = self.m - 1 - i
    
    def search(self, text):
        """
        Cerca il pattern nel testo usando FBAS.
        Ritorna: indice della prima occorrenza o -1 se non trovato
        """
        self.comparisons = 0
        n = len(text)
        
        if n < self.m:
            return -1
        
        current_idx = 0
        
        while current_idx <= n - self.m:
            # OTTIMIZZAZIONE CHIAVE: controlla prima l'ancora (carattere raro)
            text_anchor_pos = current_idx + self.anchor_idx
            self.comparisons += 1
            
            if text[text_anchor_pos] == self.anchor_char:
                # Match dell'ancora! Ora controlla il resto del pattern
                match = True
                for i in range(self.m):
                    if i == self.anchor_idx:
                        continue  # Ancora già controllata
                    self.comparisons += 1
                    if text[current_idx + i] != self.pattern[i]:
                        match = False
                        break
                if match:
                    return current_idx  # Match completo trovato
            
            # Calcola il salto usando Bad Character Heuristic
            char_at_end = text[current_idx + self.m - 1] if current_idx + self.m - 1 < n else None
            
            if char_at_end in self.shift_table:
                step = self.shift_table[char_at_end]
            else:
                step = self.m
            
            current_idx += step
        
        return -1
    
    def get_comparisons(self):
        return self.comparisons
    
    def get_anchor_info(self):
        """Ritorna informazioni sull'ancora scelta"""
        return {
            'char': self.anchor_char,
            'index': self.anchor_idx,
            'frequency_score': self.freq_table.get(self.anchor_char.lower(), 50)
        }