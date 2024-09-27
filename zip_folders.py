import os
import zipfile
import shutil

def remove_existing_zip(zip_file_name):
    """Remove o arquivo ZIP se ele já existir."""
    if os.path.exists(zip_file_name):
        os.remove(zip_file_name)
        print(f"Arquivo {zip_file_name} removido.")
    else:
        print(f"Arquivo {zip_file_name} não encontrado.")


def zip_folder(folder_name):
    zip_file_name = f"{folder_name}.zip"

    remove_existing_zip(zip_file_name)

    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_name):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, os.path.join(folder_name, '..')))

    print(f"Pasta {folder_name} foi compactada em {zip_file_name}.")


def remove_folder(folder_name):
    """Exclui a pasta após compactação."""
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
        print(f"Pasta {folder_name} foi excluída.")
    else:
        print(f"A pasta {folder_name} não foi encontrada para exclusão.")


def main():
    folders_to_zip = ['Homem', 'Mulher', 'Solicitantes']

    for folder in folders_to_zip:
        if os.path.exists(folder):
            zip_folder(folder)
            remove_folder(folder)
        else:
            print(f"A pasta {folder} não foi encontrada.")


if __name__ == "__main__":
    main()
