import urllib.request
import ssl
import matplotlib.pyplot as plt
import numpy as np
from naive import NaiveMatcher
from kmp import KMPMatcher
from bmh import BMHMatcher
from fbas import FBASMatcher

def download_divina_commedia():
    """Scarica la Divina Commedia dal web"""
    print("Download Divina Commedia...")
    url = "https://dmf.unicatt.it/~della/pythoncourse18/commedia.txt"
    try:
        # Crea un contesto SSL che non verifica i certificati (per compatibilità macOS)
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as response:
            text = response.read().decode('utf-8')
        print(f"✓ Testo caricato: {len(text):,} caratteri\n")
        return text
    except Exception as e:
        print(f"✗ Errore nel download: {e}")
        return None

def test_single_pattern(text, pattern):
    """Testa tutti gli algoritmi su un singolo pattern"""
    print(f"\n{'='*70}")
    print(f"Pattern: '{pattern}' (lunghezza: {len(pattern)})")
    print(f"{'='*70}")
    
    result = {
        'pattern': pattern,
        'length': len(pattern)
    }
    
    # Test Naive
    naive = NaiveMatcher(pattern)
    pos_naive = naive.search(text)
    result['naive_comparisons'] = naive.get_comparisons()
    result['naive_found'] = pos_naive
    print(f"Naive:          {naive.get_comparisons():>12,} comparazioni")
    
    # Test KMP
    kmp = KMPMatcher(pattern)
    pos_kmp = kmp.search(text)
    result['kmp_comparisons'] = kmp.get_comparisons()
    result['kmp_found'] = pos_kmp
    print(f"KMP:            {kmp.get_comparisons():>12,} comparazioni")
    
    # Test BMH
    bmh = BMHMatcher(pattern)
    pos_bmh = bmh.search(text)
    result['bmh_comparisons'] = bmh.get_comparisons()
    result['bmh_found'] = pos_bmh
    print(f"BMH:            {bmh.get_comparisons():>12,} comparazioni")
    
    # Test FBAS
    fbas = FBASMatcher(pattern)
    pos_fbas = fbas.search(text)
    anchor_info = fbas.get_anchor_info()
    result['fbas_comparisons'] = fbas.get_comparisons()
    result['fbas_found'] = pos_fbas
    result['fbas_anchor'] = anchor_info['char']
    result['fbas_anchor_idx'] = anchor_info['index']
    print(f"FBAS:           {fbas.get_comparisons():>12,} comparazioni")
    print(f"                (ancora: '{anchor_info['char']}' pos {anchor_info['index']}, " +
          f"rarità: {anchor_info['frequency_score']})")
    
    # Calcola miglioramenti
    if result['bmh_comparisons'] > 0:
        improvement_vs_bmh = ((result['bmh_comparisons'] - result['fbas_comparisons']) / 
                               result['bmh_comparisons'] * 100)
        result['improvement_vs_bmh'] = improvement_vs_bmh
        
        symbol = "✓" if improvement_vs_bmh > 0 else "✗"
        print(f"\n{symbol} FBAS vs BMH:  {improvement_vs_bmh:+.2f}% comparazioni")
    
    if result['naive_comparisons'] > 0:
        improvement_vs_naive = ((result['naive_comparisons'] - result['fbas_comparisons']) / 
                                 result['naive_comparisons'] * 100)
        result['improvement_vs_naive'] = improvement_vs_naive
    
    return result

def test_all_patterns(text, patterns):
    """Testa tutti i pattern"""
    results = []
    for pattern in patterns:
        result = test_single_pattern(text, pattern)
        results.append(result)
    return results

def plot_comparison_charts(results):
    """Genera i grafici di confronto"""
    print("\n" + "="*70)
    print("GENERAZIONE GRAFICI")
    print("="*70)
    
    patterns = [r['pattern'][:15] + '...' if len(r['pattern']) > 15 else r['pattern'] 
                for r in results]
    
    naive_comp = [r['naive_comparisons'] for r in results]
    kmp_comp = [r['kmp_comparisons'] for r in results]
    bmh_comp = [r['bmh_comparisons'] for r in results]
    fbas_comp = [r['fbas_comparisons'] for r in results]
    
    # Grafico 1: Confronto generale tutti gli algoritmi
    fig, ax = plt.subplots(figsize=(14, 7))
    
    x = np.arange(len(patterns))
    width = 0.2
    
    ax.bar(x - 1.5*width, naive_comp, width, label='Naive', 
           color='#e74c3c', alpha=0.85, edgecolor='black', linewidth=0.5)
    ax.bar(x - 0.5*width, kmp_comp, width, label='KMP', 
           color='#3498db', alpha=0.85, edgecolor='black', linewidth=0.5)
    ax.bar(x + 0.5*width, bmh_comp, width, label='BMH', 
           color='#f39c12', alpha=0.85, edgecolor='black', linewidth=0.5)
    ax.bar(x + 1.5*width, fbas_comp, width, label='FBAS', 
           color='#2ecc71', alpha=0.85, edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('Pattern', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Comparisons', fontsize=13, fontweight='bold')
    ax.set_title('Pattern Matching Algorithms Comparison - Divina Commedia', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(patterns, rotation=45, ha='right', fontsize=10)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('1_comparison_all_algorithms.png', dpi=300, bbox_inches='tight')
    print("✓ Salvato: 1_comparison_all_algorithms.png")
    plt.close()
    
    # Grafico 2: Focus BMH vs FBAS
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.bar(x - 0.2, bmh_comp, 0.4, label='BMH (Gold Standard)', 
           color='#f39c12', alpha=0.85, edgecolor='black', linewidth=0.5)
    ax.bar(x + 0.2, fbas_comp, 0.4, label='FBAS (New)', 
           color='#2ecc71', alpha=0.85, edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('Pattern', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Comparisons', fontsize=13, fontweight='bold')
    ax.set_title('FBAS vs BMH - Direct Comparison', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(patterns, rotation=45, ha='right', fontsize=10)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('2_fbas_vs_bmh.png', dpi=300, bbox_inches='tight')
    print("✓ Salvato: 2_fbas_vs_bmh.png")
    plt.close()
    
    # Grafico 3: Miglioramento percentuale FBAS vs BMH
    improvements = [r.get('improvement_vs_bmh', 0) for r in results]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = ['#2ecc71' if imp > 0 else '#e74c3c' for imp in improvements]
    bars = ax.bar(patterns, improvements, color=colors, alpha=0.85, 
                   edgecolor='black', linewidth=0.5)
    
    # Aggiungi valori sulle barre
    for i, (bar, imp) in enumerate(zip(bars, improvements)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{imp:+.1f}%',
                ha='center', va='bottom' if height > 0 else 'top',
                fontsize=9, fontweight='bold')
    
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.set_xlabel('Pattern', fontsize=13, fontweight='bold')
    ax.set_ylabel('Improvement (%)', fontsize=13, fontweight='bold')
    ax.set_title('FBAS: Percentage Improvement vs BMH', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('3_improvement_percentage.png', dpi=300, bbox_inches='tight')
    print("✓ Salvato: 3_improvement_percentage.png")
    plt.close()
    
    # Grafico 4: Speedup rispetto a Naive
    fig, ax = plt.subplots(figsize=(14, 7))
    
    speedup_kmp = [naive_comp[i] / kmp_comp[i] if kmp_comp[i] > 0 else 0 
                   for i in range(len(results))]
    speedup_bmh = [naive_comp[i] / bmh_comp[i] if bmh_comp[i] > 0 else 0 
                   for i in range(len(results))]
    speedup_fbas = [naive_comp[i] / fbas_comp[i] if fbas_comp[i] > 0 else 0 
                    for i in range(len(results))]
    
    x = np.arange(len(patterns))
    width = 0.25
    
    ax.bar(x - width, speedup_kmp, width, label='KMP', 
           color='#3498db', alpha=0.85, edgecolor='black', linewidth=0.5)
    ax.bar(x, speedup_bmh, width, label='BMH', 
           color='#f39c12', alpha=0.85, edgecolor='black', linewidth=0.5)
    ax.bar(x + width, speedup_fbas, width, label='FBAS', 
           color='#2ecc71', alpha=0.85, edgecolor='black', linewidth=0.5)
    
    ax.axhline(y=1, color='red', linestyle='--', linewidth=1, label='Baseline (Naive)')
    ax.set_xlabel('Pattern', fontsize=13, fontweight='bold')
    ax.set_ylabel('Speedup (times faster than Naive)', fontsize=13, fontweight='bold')
    ax.set_title('Speedup compared to Naive Algorithm', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(patterns, rotation=45, ha='right', fontsize=10)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('4_speedup_vs_naive.png', dpi=300, bbox_inches='tight')
    print("✓ Salvato: 4_speedup_vs_naive.png")
    plt.close()

def print_final_statistics(results):
    """Stampa statistiche finali"""
    print("\n" + "="*70)
    print("STATISTICHE FINALI")
    print("="*70)
    
    total_naive = sum(r['naive_comparisons'] for r in results)
    total_kmp = sum(r['kmp_comparisons'] for r in results)
    total_bmh = sum(r['bmh_comparisons'] for r in results)
    total_fbas = sum(r['fbas_comparisons'] for r in results)
    
    print(f"\nTOTALE COMPARAZIONI (somma di tutti i pattern):")
    print(f"  Naive:  {total_naive:>15,}")
    print(f"  KMP:    {total_kmp:>15,}")
    print(f"  BMH:    {total_bmh:>15,}")
    print(f"  FBAS:   {total_fbas:>15,}")
    
    print(f"\nMIGLIORAMENTO MEDIO:")
    avg_improvement_bmh = np.mean([r.get('improvement_vs_bmh', 0) for r in results])
    avg_improvement_naive = np.mean([r.get('improvement_vs_naive', 0) for r in results])
    
    print(f"  FBAS vs BMH:   {avg_improvement_bmh:+.2f}%")
    print(f"  FBAS vs Naive: {avg_improvement_naive:+.2f}%")
    
    # Conta vittorie
    wins_vs_bmh = sum(1 for r in results if r.get('improvement_vs_bmh', 0) > 0)
    print(f"\nVITTORIE FBAS vs BMH: {wins_vs_bmh}/{len(results)} pattern")
    
    print("\n" + "="*70)

def main():
    """Funzione principale"""
    print("="*70)
    print("CONFRONTO ALGORITMI DI PATTERN MATCHING")
    print("FBAS vs Naive vs KMP vs Boyer-Moore-Horspool")
    print("="*70)
    
    # Download testo
    text = download_divina_commedia()
    if text is None:
        print("Impossibile procedere senza il testo.")
        return
    
    # Pattern di test
    test_patterns = [
        "inferno",       # Comune, parola chiave
        "paradiso",      # Comune, parola chiave
        "purgatorio",    # Meno comune
        "beatrice",      # Nome proprio
        "dante",         # Nome proprio, breve
        "virtute",       # Contiene 'u' rara
        "canoscenza",    # Pattern più lungo
        "nel mezzo",     # Frase breve con spazio
        "selva oscura",  # Frase con spazio
        "amor",          # Molto comune
        "luce",          # Comune
        "dolce"          # Comune
    ]
    
    print(f"Pattern da testare: {len(test_patterns)}")
    
    # Esegui test
    results = test_all_patterns(text, test_patterns)
    
    # Genera grafici
    plot_comparison_charts(results)
    
    # Stampa statistiche
    print_final_statistics(results)
    
    print("\n✓ ANALISI COMPLETATA CON SUCCESSO")
    print("  Controlla i file PNG generati nella directory corrente.")
    print("="*70)

if __name__ == "__main__":
    main()