import os


def create_decade_corpus(corpus, start_year):
    decade_directory = "./results"
    try:
        os.mkdir(decade_directory)
        print(f"Directory '{decade_directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{decade_directory}' already exists.")

    with open(f'{decade_directory}/{start_year}_decade_mzk_books.txt', 'w', encoding='utf-8') as corpus_file:
        print(corpus, file=corpus_file)
