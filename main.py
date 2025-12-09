import raw_data_loader
import data_saver
from corpus_tools import decades_stats
from visualizers import basic_ploter, word_evolution_plotter


def test_corpora():
    start_year = 1850
    decade_directory = "../mzkscraper/results/decades/" + str(start_year) + "decade"
    decade_corpus = raw_data_loader.load_decade(decade_directory)
    data_saver.create_decade_corpus(decade_corpus, f'{start_year}_old')

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


# test_corpora()

# assemble_corpora()

#decades_stats.collect_decade_stats(output_file = "decades_stats_cz.tsv")
# decades_stats.collect_decade_wordfreqs(startswith="1850")
# basic_ploter.plot_decade_stats(log_scale=False, stats_file = "./data_outputs/decades_stats_cz.tsv")
#basic_ploter.heaps_law_fit(stats_file = "./data_outputs/decades_stats_cz.tsv")
#
#
# # word_to_plot = ["hned", "ihned"]
# # word_to_plot = ["lučba", "chemie"]
# word_to_plot = ["urlaub", "dovolená"]
# word_to_plot = ["válka", "vojna"]
# #word_to_plot = ["rakousko", "československo", "německo"]
# #word_to_plot = ["císař", "prezident", "president", "král"]
#
#
# # word_to_plot = ["kráľu", "králi"]
# # word_to_plot = ["inhedž", "hned", "ihned", "inhed"]
# # word_to_plot = [ "hned", "ihned", "inhed"]
# #word_to_plot = [ "sě", "se"]
# word_to_plot = [ "lénunk", "žold"]
# # word_to_plot = [ "lénunk"]
# # word_to_plot = [ "propást"]
word_to_plot = ["nejmnožší"]
word_evolution_plotter.plot_word_frequencies(word_to_plot)