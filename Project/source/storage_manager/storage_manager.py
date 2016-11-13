import pickle

MANUAL_PATH = "storage/program_data/manual"
PROPOSED_CHANGES_PATH = "storage/program_data/CHANGES_STORAGE"
CONFIG_PATH = "storage/program_data/program_config"
ENCODING = "ASCII"

def manual():
    return read_file(MANUAL_PATH)

def read_file(path):
    s = ""
    f = open(path, "r")
    for line in f:
        s += line
    f.close()
    return s


def write_changes_to_memory(changes_list):
    with open(PROPOSED_CHANGES_PATH, "wb") as File:
        pickle.dump(changes_list, File)


def read_changes_from_memory():
    '''
    PROPOSED_CHANGES_PATH determines the path to write to.
    
    Throws EOFError if file is empty.
    Throws FileNotFoundError if file DNE.
    '''
    with open(PROPOSED_CHANGES_PATH, "rb") as File:
        try:
            changes_list = pickle.load(File, encoding=ENCODING)
        # if the storage file is empty, return an empty list
        except EOFError:
            changes_list = []
    return changes_list


def clean_config_file():
    '''
    Resets the config file to its original clean state.    
    
    
    Keys present in the dictionary by default:
    
    "last_update" -> str : time of last update (Default : "Never")
    '''
    content = {}
    content["last_update"] = "Never"
    with open(CONFIG_PATH, "wb") as File:
        pickle.dump(content, File)    


def config_set(key, val):
    '''
    If the config file is empty or unreadable for any reason, returns None and
    calls clean_config_file() to reset it to default state.
    '''
    reset = False
    with open(CONFIG_PATH, "rb") as File:
        try:
            config_dict = pickle.load(File, encoding=ENCODING)
        # if the storage file is unreadable, reset the file to default state
        except EOFError:
            reset = True
            config_dict = None
    if reset:
        clean_config_file()
        with open(CONFIG_PATH, "rb") as File:
            config_dict = pickle.load(File, encoding=ENCODING)
    config_dict[key] = val
    with open(CONFIG_PATH, "wb") as File:
        pickle.dump(config_dict, File)


def config_get(key):
    '''
    If the config file is empty or unreadable for any reason, returns None and
    calls clean_config_file() to reset it to default state.
    '''
    reset = False
    with open(CONFIG_PATH, "rb") as File:
        try:
            config_dict = pickle.load(File, encoding=ENCODING)
            result = config_dict.get(key)
        # if the storage file is unreadable, return None, reset the file to
        # default state
        except EOFError:
            result = None
            reset = True
    if reset:
        clean_config_file()
    return result


if __name__ == "__main__" :
    '''
    # Test code block to ensure that the changes are stored in memory and 
    # retrieved correctly
    PROPOSED_CHANGES_PATH = "../" + PROPOSED_CHANGES_PATH
    changes_list = read_changes_from_memory()
    print(len(changes_list))
    i = 0
    while i < len(changes_list):
        #print("\nShowing number : " + str(i + 1) + "\n")
        #print(changes_list[i])
        #print()
        i += 1
    '''
    CONFIG_PATH = "../" + CONFIG_PATH
    clean_config_file()
    