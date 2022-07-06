import sys, os, signal, requests, re, bs4


def progress_bar(i) -> int:
    if i == 0:
        print("working \ō͡≡o˞̶")
    else:
        #erasing upper line
        sys.stdout.write('\x1b[1A\x1b[2K')
        #progress bar
        print("working", " " * (i % 25), "\ō͡≡o˞̶")
    i += 1
    return i


def main() -> int:
    #creating a child
    pid = os.fork()

    #Parent:
    if pid:
        stoped = False
        cont = True
        print("type: k - to kill, s - to suspend, c - to wake up")
        while True:
            i = input()
            if   i == 'k':
                #killing the child ψ(｀∇´)ψ
                os.kill(pid, signal.SIGKILL)
                os.system('clear')
                print("killed sucsefully  (⌣́_⌣̀)")
                sys.exit(0)
            elif i == 's':
                #suspending the child (¯﹃¯)
                if not stoped:
                    os.kill(pid, signal.SIGSTOP)
                    stoped = True
                    cont = False
                    os.system('clear')
                    print("type: k - to kill, s - to suspend, c - to wake up\nsuspended sucsefully ꒰ ᵕ༚ᵕ꒱ ˖°")
            elif i == 'c':
                #awakening the child (ಠ¿ಠ)
                if not cont:
                    os.kill(pid, signal.SIGCONT)
                    stoped = False
                    cont = True
                    os.system('clear')
                    print("type: k - to kill, s - to suspend, c - to wake up\nawakened sucsefully ᕕ( ಠ‿ಠ )ᕗ")
                    print(' ')

    #Child:
    else:
        with open("queries.txt") as file:
            strings = [line.rstrip() for line in file]

        #cleaning from empty strings and replacing space with +
        clean_strings = []
        for line in strings:
            if line.strip():
                line = line.replace(' ', '+')
                clean_strings.append(line)

        #trying to read previous position
        try:
            with open("position.txt") as file:
                i = int(file.read().strip())
        except:
            i = 1

        progress = 0 #needed for progress bar
        while True:
            #printing progress bar
            progress = progress_bar(progress)
            link = "https://www.google.com/search?q="
            #getting search strings
            search = (clean_strings[i % len(clean_strings)])
            r = requests.get(link + search)
            #creating BeautifulSoup object, which represents html file
            soup = bs4.BeautifulSoup(r.content,features="lxml")
            #searching for links in html response from google
            with open("search.txt", 'a') as f:
                links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
                for i in range(0, len(links) - 2): #last two links are accounts.google.com, support.google.com
                        #writing links to a file
                        f.write((re.split(":(?=http)",links[i]["href"].replace("/url?q=","")))[0])
                        f.write("\n")           
            i += 1
            #writing position to a file
            with open("position.txt", "w") as file:
                file.write(str(i))

if __name__ == "__main__":
    sys.exit(main()) 