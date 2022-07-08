import sys, os, search, ui, threading
from unittest import runner

class thread(threading.Thread):
    def __init__(self, cpid, ppid) -> None:
        super().__init__()
        self.cpid = cpid
        self.ppid = ppid
        self.ui = ui.ui(cpid, ppid)
    
    def run(self):
        while True:
            self.ui.get_input()

def main() -> int:
    #creating a child
    pid = os.fork()
    #Parent:
    if pid:
        thread1 = thread(pid, os.getpid())
        thread1.start()
        os.wait()
        return 0
    #Child:
    else:
        searchg = search.search(queries_file="queries.txt", position=0)
        searchg.google_search(-2, -5)
        

if __name__ == "__main__":
    sys.exit(main()) 