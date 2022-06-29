import sys
import time

def main() -> int:
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
        with open("position.txt", "w") as position:
            position.write(str(i))
        time.sleep(1)
    return 0

if __name__ == "__main__":
    sys.exit(main())