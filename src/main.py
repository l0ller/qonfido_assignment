from download import main as download_main
from parser import parse_all
from normalize import normalize_all

def main():
    download_main()      # step 1: API download
    parse_all()    # step 2: parse + merge
    normalize_all() # step 3: clean + normalize
if __name__ == "__main__":
    main()
