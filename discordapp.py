import os
import re


def affinites():
    chemin = os.getenv('APPDATA') + '\\Discord' + '\\Local Storage\\leveldb'
    hits = []
    for fichier in os.listdir(chemin):
        if not fichier.endswith('.log') and not fichier.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{chemin}\\{fichier}', errors='ignore').readlines() if x.strip()]:
            for regex in r'affinity':
                for hit in re.findall(regex, line):
                    hits.append(hit)
        return hits


def afficher():
    result = affinites()
    if len(result) == 0:
        print("Vous n'avez pas de fichier d'affinités, désolé")
        return
    print(result)


afficher()
