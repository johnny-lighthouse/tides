import tides

con,cur = tides.initiate_db()

tides.get_and_store(con,cur)

extract = tides.extract_all_data(cur)
