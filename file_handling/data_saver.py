import os


def create_decade_corpus(corpus, start_year):
    corpus = "\n".join(corpus)
    decade_directory = "./results"
    try:
        os.mkdir(decade_directory)
        print(f"Directory '{decade_directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{decade_directory}' already exists.")

    with open(f'{decade_directory}/{start_year}_decade_mzk_books.txt', 'w', encoding='utf-8') as corpus_file:
        print(corpus, file=corpus_file)
        print(f"/{start_year}_decade_mzk_books.txt created successfully.")


def create_decade_clean_ocrs(documents, f_names, start_year):
    decade_directory = "./results"
    try:
        os.mkdir(decade_directory)
        print(f"Directory '{decade_directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{decade_directory}' already exists.")

    decade_directory = f"./results/{start_year}"
    try:
        os.mkdir(decade_directory)
        print(f"Directory '{decade_directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{decade_directory}' already exists.")
    for doc, f_name in zip(documents, f_names):
        with open(f'{decade_directory}/{f_name}.ccr', 'w', encoding='utf-8') as corpus_file:
            print(doc, file=corpus_file)
