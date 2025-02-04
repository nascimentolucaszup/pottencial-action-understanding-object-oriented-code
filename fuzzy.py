from rapidfuzz import process, fuzz
from utils.loads import load_data

def find_similar_matches(query, files, threshold=60):
    # Extrai os nomes dos arquivos para comparação
    file_names = [file["file_name"] for file in files]
    
    # Usa o método process para encontrar todas as correspondências acima do threshold
    matches = process.extract(
        query,  # Query de entrada
        file_names,  # Lista de strings para comparar
        scorer=fuzz.token_set_ratio,  # Scorer para medir similaridade
        score_cutoff=threshold,  # Limite mínimo de similaridade
        limit=10,
    )
    
    # Retorna os objetos correspondentes às correspondências encontradas
    results = []
    for match in matches:
        matched_file_name, score, index = match
        results.append({
            "match": files[index],
            "score": score
        })
    
    return results

# Exemplo de uso
query = "LimiteTaxa"
result = find_similar_matches(query, load_data("file-to-analyze/index.json"))

if result:
    print("Correspondências encontradas:")
    for match in result:
        print(f"Arquivo: {match['match']['file_name']}, Similaridade: {match['score']}%")
else:
    print("Nenhuma correspondência encontrada.")