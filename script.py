import os


def replace_paths(directory):
    for root, dirs, files in os.walk(directory):
        print(f"Traitement du dossier : {root}")
        for file in files:
            if file.endswith('.jsx') or file.endswith('.js'):
                file_path = os.path.join(root, file)

                # Lire le contenu du fichier
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Effectuer les remplacements
                new_content = content.replace('../../components', '../components')
                new_content = new_content.replace('../../lib', '../lib')

                # Écrire le contenu modifié dans le fichier si des changements ont été effectués
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Modifié : {file_path}")
                else:
                    print(f"Aucun changement : {file_path}")
            else:
                print(f"Ignoré (pas un fichier .jsx) : {os.path.join(root, file)}")


# Spécifiez le chemin du dossier ici
folder_path = 'E:\\newDev\\website\\original-pledge-and-grow\\src\\components'
replace_paths(folder_path)
