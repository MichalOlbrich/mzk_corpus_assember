
from corpus_creation import corpus_assembler
from visualizers import word_evolution_plotter, basic_ploter
from corpus_tools import decades_stats

# corpus_assembler.test_corpus()

# corpus_assembler.assemble_corpora()

# decades_stats.collect_decade_stats(output_file = "decades_stats_unfiltered.tsv")
# decades_stats.collect_decade_wordfreqs(startswith="1850")

# basic_ploter.plot_decade_stats(log_scale=False, stats_file = "./data_outputs/decades_stats_cz.tsv")
# basic_ploter.plot_decade_stats_comparison(log_scale=True)
# basic_ploter.plot_decade_stats_comparison(log_scale=True,unfiltered_stats_file="./data_outputs/decades_stats_diakon.tsv")
# basic_ploter.plot_decade_unique_stats(log_scale=False)
#basic_ploter.heaps_law_fit(stats_file = "./data_outputs/decades_stats_cz.tsv")
#
#
# # word_to_plot = ["hned", "ihned"]
# # word_to_plot = ["lučba", "chemie"]
# word_to_plot = ["urlaub", "dovolená"]
# word_to_plot = ["válka", "vojna"]
# word_to_plot = ["jenerál", "generál"]


# #word_to_plot = ["rakousko", "československo", "německo"]
# #word_to_plot = ["císař", "prezident", "president", "král"]
#
#
# # word_to_plot = ["inhedž", "hned", "ihned", "inhed"]
# # word_to_plot = [ "hned", "ihned", "inhed"]
# #word_to_plot = [ "sě", "se"]
# word_to_plot = [ "lénunk", "žold"]
# # word_to_plot = [ "lénunk"]
# # word_to_plot = [ "propást"]
# word_to_plot = ["nejmnožší"]
word_to_plot = ["jest", "je"]
#
word_evolution_plotter.plot_word_frequencies(word_to_plot)