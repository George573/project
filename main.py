import sys, os, search, ui, threading

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
        '''test input
        searchg = search.search(queries_file="queries.txt", position="1", start_over=True, links_file=1, position_file="nope.tx")
        searchg.google_search("4", -1, "hi")
        '''
        #normal input
        searchg = search.search(queries_file="queries.txt", start_over=True)
        searchg.google_search(1, 4, 0.5)
        

if __name__ == "__main__":
    sys.exit(main()) 