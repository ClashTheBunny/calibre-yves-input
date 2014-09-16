from subprocess import Popen, PIPE

def plistFromFile(filename,type):
    "Pipe the binary plist file through plutil and parse the JSON output"
    with open(filename, "rb") as f:
        content = f.read()
    return plistFromString(content,type)

def plistFromString(content,type):
    "Pipe the binary plist string through plutil and parse the output"
    args = ["plutil", "-convert", type, "-o", "-", "--", "-"]
    p = Popen(args, stdin=PIPE, stdout=PIPE)
    p.stdin.write(content)
    out, err = p.communicate()
    return out
