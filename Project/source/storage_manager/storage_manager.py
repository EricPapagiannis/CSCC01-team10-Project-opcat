import pickle

DEFAULT_REPO_URL \
    = "https://github.com/EricPapagiannis/open_exoplanet_catalogue.git"
MANUAL_PATH = "storage/program_data/manual"
PROPOSED_CHANGES_PATH = "storage/program_data/CHANGES_STORAGE"
CONFIG_PATH = "storage/program_data/program_config"
ENCODING = "ASCII"


def manual():
    '''
    () -> str
    
    Returns the manual for the application stored in a plaintext file, whose
    path is declared above.
    '''
    return read_file(MANUAL_PATH)


def read_file(path):
    '''
    (str) -> str

    Takes path (str) to a plaintext file and returns its contents as a single
    string.
    
    path must point to an existing plaintext file
    '''
    s = ""
    f = open(path, "r")
    # accumulate the contents of the file in the string s
    for line in f:
        s += line
    f.close()
    return s


def write_changes_to_memory(changes_list):
    '''
    ([ProposedChange]) -> None
    
    Takes a list of ProposedChanges and stores it on the hard drive in order to
    retain it between the invocations of the program.
    PROPOSED_CHANGES_PATH determines the path to write to.
    '''
    with open(PROPOSED_CHANGES_PATH, "wb") as File:
        pickle.dump(changes_list, File)


def read_changes_from_memory():
    '''
    () -> [ProposedChange]
    
    Reads the list of proposed changes from the memory and returns it.
    PROPOSED_CHANGES_PATH determines the path to read from.
    
    Throws EOFError if file is empty.
    Throws FileNotFoundError if file DNE.
    '''
    try:
        with open(PROPOSED_CHANGES_PATH, "rb") as File:
            changes_list = pickle.load(File, encoding=ENCODING)
    # if the storage file is empty, return an empty list
    except (EOFError, FileNotFoundError) as e:
        changes_list = []
    return changes_list


def clean_config_file():
    '''
    () - > None
    
    Resets the config file to its original clean state.    
    
    Keys present in the dictionary by default:
    
    "last_update" -> str : time of last update (Default : "Never")
    "black_list" -> [] : the storage of ProposedChange objects declined by the
    user
    "auto_update_settings" -> None for never | int for number of hours between
    updates
    '''
    global DEFAULT_REPO_URL
    content = {}
    # set the required fields to their default value
    content["last_update"] = "Never"
    content["black_list"] = []
    content["auto_update_settings"] = None
    content["repo_url"] = DEFAULT_REPO_URL
    content["branch_number"] = 1
    with open(CONFIG_PATH, "wb") as File:
        pickle.dump(content, File)


def config_set(key, val):
    '''
    (key, value) -> None
    
    Sets the key given as param in the config dictionary in memory to the value
    "value". The dictionary is retained after the process terminates.
    
    If the config file is empty or unreadable for any reason, returns None and
    calls clean_config_file() to reset it to default state.
    '''
    reset = False
    try:
        with open(CONFIG_PATH, "rb") as File:
            config_dict = pickle.load(File, encoding=ENCODING)
    # if the storage file is unreadable, reset the file to default state
    except (EOFError, FileNotFoundError) as e:
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
    (str) -> object

    Returns the value for the key "key" from the config dictionary.
    
    If the config file is empty or unreadable for any reason, returns None and
    calls clean_config_file() to reset it to default state.
    '''
    reset = False
    try:
        with open(CONFIG_PATH, "rb") as File:
            config_dict = pickle.load(File, encoding=ENCODING)
            result = config_dict.get(key)
    # if the storage file is unreadable, return None, reset the file to default
    # state
    except (EOFError, FileNotFoundError) as e:
        result = None
        reset = True
    if reset:
        clean_config_file()
    return result


def reset_to_default():
    '''
    () -> None
    
    Returns all program configurations to default state, which includes: (1) - 
    clearing the stored list of proposed changes, and (2) - resetting the 
    config file to default configuration.
    '''
    write_changes_to_memory([])
    clean_config_file()


if __name__ == "__main__":
    MANUAL_PATH = "../" + MANUAL_PATH
    PROPOSED_CHANGES_PATH = "../" + PROPOSED_CHANGES_PATH
    CONFIG_PATH = "../" + CONFIG_PATH
    reset_to_default()
