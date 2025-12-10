from file_handling import data_saver, raw_data_loader
from corpus_creation import corpus_cleaner

def test_corpora():
    start_year = 1870
    decade_directory = "../mzkscraper/results/decades/" + str(start_year) + "decade"
    raw_documents = raw_data_loader.load_decade(decade_directory)
    decade_corpus = corpus_cleaner.cleanup_and_create_decade_corpus(raw_documents)
    # data_saver.create_decade_corpus(decade_corpus, f'{start_year}_old')

def assemble_corpora():
    # start_year = 1880
    # decade_directory = "../mzkscraper/results/decades/" + str(start_year) + "decade"
    # decade_corpus = raw_data_loader.load_decade(decade_directory)
    # data_saver.create_decade_corpus(decade_corpus, start_year)
    start_year = 1870
    for decade in range(start_year,1950,10):
        decade_directory = "../mzkscraper/results/decades/" + str(decade) + "decade"
        decade_corpus = raw_data_loader.load_decade(decade_directory)
        data_saver.create_decade_corpus(decade_corpus, decade)
