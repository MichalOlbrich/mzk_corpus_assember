from file_handling import data_saver, raw_data_loader
from corpus_creation import corpus_cleaner

def test_corpus():
    start_year = 1850
    decade_directory = "../mzkscraper/results/decades/" + str(start_year) + "decade"
    raw_documents, file_names = raw_data_loader.load_decade(decade_directory)
    clean_documents, f_names, recovery_measures = corpus_cleaner.cleanup_and_create_decade_corpus(raw_documents, file_names)
    # data_saver.create_decade_corpus(clean_documents, f'{start_year}_filtered')
    data_saver.create_decade_clean_ocrs(clean_documents,f_names, start_year)

def assemble_corpora():

    start_year = 1850
    for decade in range(start_year,1950,10):
        decade_directory = "../mzkscraper/results/decades/" + str(decade) + "decade"
        raw_documents, file_names = raw_data_loader.load_decade(decade_directory)
        # clean_documents, f_names, recovery_measures = corpus_cleaner.cleanup_and_create_decade_corpus(raw_documents,
        #                                                                                             file_names)
        data_saver.create_decade_corpus(raw_documents, f'{decade}_unfiltered')
