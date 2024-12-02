'''
    Get all data from csv here in functions
'''

# example 
def get_ratings() -> np.array:
    '''
        Returns rating table
    '''

    rating_df = pd.read_csv("your_path.csv")

    # Renaming data here
    ...

    return rating_df