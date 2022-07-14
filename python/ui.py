import os, sys, signal

class Ui:
    def __init__(self, cpid, ppid) -> None:
        self.cpid = cpid
        self.ppid = ppid
        self.stoped = False
        self.cont = True
        print("type: k - to kill, s - to suspend, c - to wake up")

    def get_input(self):
        inp = input()
        if   inp == 'k':
            # killing the child ψ(｀∇´)ψ
            self.kill_kid()
        elif inp == 's':
            # suspending the child (¯﹃¯)
            self.suspend_kid()
        elif inp == 'c':
            # awakening the child (ಠ¿ಠ)
            self.continue_kid()
        elif inp == 'e':
            self.exit()
   
    def kill_kid(self):
        os.kill(self.cpid, signal.SIGKILL)
        os.system('clear')
        print("killed sucsefully  (⌣́_⌣̀)")
        sys.exit(0)

    def suspend_kid(self):
        if not self.stoped:
            os.kill(self.cpid, signal.SIGSTOP)
            self.stoped = True
            self.cont = False
            os.system('clear')
            print("type: k - to kill, s - to suspend, c - to wake up\nsuspended sucsefully ꒰ ᵕ༚ᵕ꒱ ˖°")

    def continue_kid(self):
        if not self.cont:
            os.kill(self.cpid, signal.SIGCONT)
            self.stoped = False
            self.cont = True
            os.system('clear')
            print("type: k - to kill, s - to suspend, c - to wake up\nawakened sucsefully ᕕ( ಠ‿ಠ )ᕗ")
            print(' ')

    def exit(self):
        sys.exit(0)