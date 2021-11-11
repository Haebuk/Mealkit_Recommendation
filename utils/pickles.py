import pickle

def write_pickle_files(data, file_name):
    """
    Write data to pickle files
    """
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)

def read_pickle_files(file_name):
    """
    Read pickle files
    """
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    return data