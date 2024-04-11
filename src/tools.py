def read_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

def fatal_error(message):
    print("Fatal error:", message)
    exit()
