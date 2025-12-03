import raw_data_loader


start_year = 1890
decade_directory = "../mzkscraper/results/decades/" + str(start_year) + "decade"
raw_data_loader.load_decade(decade_directory)