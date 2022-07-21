import sys, os, search, ui, threading

class Thread(threading.Thread):
    def __init__(self, cpid : int, ppid : int) -> None:
        super().__init__()
        self.cpid = cpid
        self.ppid = ppid
        self.ui = ui.Ui(cpid, ppid)

    def run(self):
        while True:
            self.ui.get_input()

def main() -> int:
    #Parent:
    if (pid := os.fork()):
        thread1 = Thread(pid, os.getpid())
        thread1.start()
        os.wait()
        print("Type 'e' to exit")
        return 0
    #Child:
    else:
        '''test input
        searchg = search.search(queries_file="queries.txt", position="1", start_over=True, links_file=1, position_file="nope.tx")
        searchg.google_search("4", -1, "hi")
        '''
        #normal input
        searchg = search.Search(queries_file="./files/queries.txt", start_over=False)
        searchg.google_search(1, 2, 0.5)
        return 0


if __name__ == "__main__":
    sys.exit(main()) 