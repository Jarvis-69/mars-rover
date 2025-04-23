import os
import re
import sys
from collections import defaultdict

# --- Fonctions Utilitaires ---

def find_cs_files(directory):
    """Trouve tous les fichiers .cs dans le répertoire donné."""
    cs_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".cs"):
                cs_files.append(os.path.join(root, file))
    return cs_files

def strip_comments_strings(text):
    """Tente de supprimer les commentaires et chaînes C# (simpliste)."""
    # Supprimer les commentaires multi-lignes /* ... */ (non-gourmand)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # Supprimer les commentaires mono-ligne // ...
    text = re.sub(r'//.*', '', text)
    # Supprimer les chaînes verbatim @"..." (simpliste, ne gère pas "")
    text = re.sub(r'@"[^"]*"', '""', text)
    # Supprimer les chaînes normales "..." (simpliste, ne gère pas \")
    text = re.sub(r'"[^"]*"', '""', text)
    return text

def extract_type_definitions(filepath):
    """Extrait les noms de types définis (class, record, etc.)."""
    names = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Lire le contenu et tenter de nettoyer commentaires/chaînes
            content = f.read()
            cleaned_content = strip_comments_strings(content)
            # Regex pour trouver les définitions de types
            pattern = r'\b(?:public|internal|private|protected)?\s*(?:static|abstract|sealed|partial)?\s*(?:class|record|struct|interface|enum)\s+(\w+)'
            matches = re.findall(pattern, cleaned_content)
            names.update(matches)
    except Exception as e:
        print(f"Warning: Could not read or parse file {filepath}: {e}", file=sys.stderr)
    return names

def find_potential_usages_refined(filepath, names_to_find):
    """Cherche des motifs d'usage plus spécifiques pour les noms de types."""
    used_names = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Tenter de nettoyer le contenu
            cleaned_content = strip_comments_strings(content)

            for name in names_to_find:
                # Motifs plus spécifiques (encore approximatifs) :
                # 1. new TypeName(...)
                # 2. TypeName.StaticMember
                # 3. : TypeName (héritage/interface)
                # 4. <TypeName> (générique)
                # 5. [TypeName] ou [TypeName(...)] (attribut)
                # 6. (TypeName) cast
                # 7. TypeName variableName (déclaration)
                pattern = r'(?:new\s+{0}\b|\b{0}\s*\.\s*\w+|:\s*{0}\b|<\s*{0}\b|\[\s*{0}\b|\(\s*{0}\s*\)|\b{0}\s+\w+)'.format(re.escape(name))
                if re.search(pattern, cleaned_content):
                    used_names.add(name)
    except Exception as e:
        print(f"Warning: Could not read or process file {filepath}: {e}", file=sys.stderr)
    return used_names

def detect_cycles(graph):
    """Détecte les cycles dans un graphe de dépendances (inchangé)."""
    path = set()
    visited = set()
    cycles = []
    def visit(node):
        path.add(node)
        visited.add(node)
        for neighbour in graph.get(node, []):
            if neighbour in path:
                try:
                    cycle_start_index = list(path).index(neighbour)
                    cycle_list = list(path)[cycle_start_index:]
                    sorted_cycle = tuple(sorted(cycle_list))
                    if sorted_cycle not in cycles:
                         cycles.append(sorted_cycle)
                except ValueError: pass
            elif neighbour not in visited:
                visit(neighbour)
        path.remove(node)
    all_nodes = list(graph.keys())
    for node in all_nodes:
        if node not in visited:
            visit(node)
    return [list(c) for c in cycles]

# --- Exécution Principale ---
if __name__ == "__main__":
    start_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"Analyzing C# files in: {start_directory}")

    cs_files = find_cs_files(start_directory)
    if not cs_files:
        print("No .cs files found.")
        sys.exit(0)

    # 1. Extraire tous les types définis
    type_definitions = defaultdict(set)
    all_defined_types = set()
    print("Extracting type definitions...")
    for f_path in cs_files:
        names = extract_type_definitions(f_path)
        for name in names:
            type_definitions[name].add(f_path)
            all_defined_types.add(name)

    # 2. Construire le graphe de dépendances (avec recherche affinée)
    dependency_graph = defaultdict(list)
    print("Building potential dependency graph (refined but still approximate)...")
    for type_name in all_defined_types:
        for defining_file in type_definitions[type_name]:
            other_types = all_defined_types - {type_name}
            # Utilisation de la fonction de recherche affinée
            potentially_used_names = find_potential_usages_refined(defining_file, other_types)
            for used_name in potentially_used_names:
                 if used_name not in dependency_graph[type_name]:
                     dependency_graph[type_name].append(used_name)

    # 3. Détecter les cycles
    print("Detecting circular dependencies...")
    cycles_found = detect_cycles(dependency_graph)

    # 4. Afficher les résultats
    if cycles_found:
        print(f"\nFound {len(cycles_found)} potential circular dependency cycle(s):")
        print("WARNING: Results are based on improved text matching but remain potentially inaccurate.")
        for i, cycle in enumerate(cycles_found):
            print(f"  Cycle {i+1}: {' -> '.join(sorted(cycle))} -> {sorted(cycle)[0]}")
    else:
        print("\nNo potential circular dependencies found based on this refined simple analysis.")

    # print("\nReminder: This script provides a basic analysis. For reliable C# dependency analysis, use dedicated .NET tools.")