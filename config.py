
bkk_coordinates = None#json.load(json_file) # boundaries of bangkok
df_distric_loc = None#pd.read_csv('../data/bkk_district_map.csv',index_col=0)  # one point location of each district # modified

df_budget = None #pd.read_pickle('../data/df_budget.pkl') # mine
df_subbudget = None#pd.read_pickle('../data/sub_budget.pkl') # mine
df_item =None
df_budget_district = None#df_budget[pd.notnull(df_budget.lat)]