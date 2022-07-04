import sys, time, os, signal, requests

def main() -> int:
    pid = os.fork()

    if pid:
        stoped = False
        cont = True
        while True:
            i = input()
            if   i == 'k':
                os.kill(pid, signal.SIGKILL)
                print("exiting")
                sys.exit(0)
            elif i == 's':
                if not stoped:
                    os.kill(pid, signal.SIGSTOP)
                    stoped = True
                    cont = False
                    print("stoped")
            elif i == 'c':
                if not cont:
                    os.kill(pid, signal.SIGCONT)
                    stoped = False
                    cont = True
                    print("continue")

    else:
        with open("queries.txt") as file:
            strings = [line.rstrip() for line in file]

        clean_strings = []
        for line in strings:
            if line.strip():
                clean_strings.append(line)
        
        try:
            with open("position.txt") as file:
                i = int(file.read().strip())
        except:
            i = 1
        
        while True:
            print(clean_strings[i % len(clean_strings)])
            i += 1
            with open("position.txt", "w") as file:
                file.write(str(i))
            time.sleep(1)

if __name__ == "__main__":
    sys.exit(main())