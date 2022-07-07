import os, sys, signal

class ui:
    def __init__(self, cpid, ppid) -> None:
        self.cpid = cpid
        self.ppid = ppid
        self.stoped = False
        self.cont = True
    
    def get_input(self):
        print("type: k - to kill, s - to suspend, c - to wake up")
        inp = input()
        if   inp == 'k':
            #killing the child ψ(｀∇´)ψ
            self.kill_kid(self.cpid)
        elif inp == 's':
            #suspending the child (¯﹃¯)
            self.suspend_kid(self.cpid)
        elif inp == 'c':
            #awakening the child (ಠ¿ಠ)
            self.continue_kid(self.cpid)
            
    def kill_kid(self, cpid):
        os.kill(cpid, signal.SIGKILL)
        os.system('clear')
        print("killed sucsefully  (⌣́_⌣̀)")
        sys.exit(0)
    
    def suspend_kid(self, cpid):
        if not self.stoped:
            os.kill(cpid, signal.SIGSTOP)
            self.stoped = True
            self.cont = False
            os.system('clear')
            print("type: k - to kill, s - to suspend, c - to wake up\nsuspended sucsefully ꒰ ᵕ༚ᵕ꒱ ˖°")

    def continue_kid(self, cpid):
        if not self.cont:
            os.kill(cpid, signal.SIGCONT)
            self.stoped = False
            self.cont = True
            os.system('clear')
            print("type: k - to kill, s - to suspend, c - to wake up\nawakened sucsefully ᕕ( ಠ‿ಠ )ᕗ")
            print(' ')