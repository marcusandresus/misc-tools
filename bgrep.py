#!/usr/bin/env python

import argparse

DEFAULTWIDTH = 80

def byte_to_str(bt):
    # remember a byte is an int 0<= x <=255
    if type(bt) == str:
        bt = ord(bt)
    if bt == 32:
        return "sp"
    elif int(bt) > 32 and int(bt) <= 127:
        return chr(bt)
    else:
        return r'\{0:02x}'.format(bt)


def dump_bytes(bs, start, length, width=None):
    if width is None:
        width = DEFAULTWIDTH
    # ln is width of column (index or value)
    ln = max(3, len(str(start + length)))
    hdr_l = [ "{0:<{1}}".format(i, ln) for i in range(start, start+length)]
    dat_l = [ "{0:<{1}}".format(byte_to_str(bs[i]), ln) for i in range(start, start+length)]
    hdr_s = " ".join(hdr_l)
    dat_s = " ".join(dat_l)
    w = width // 4
    from_i = 0
    while from_i < len(dat_s):
        to_i = from_i + 4 * w
        print(hdr_s[from_i:to_i])
        print(dat_s[from_i:to_i])
        print("")
        from_i = to_i


def main():
    parser = argparse.ArgumentParser(description="Binary Grep")
    parser.add_argument("--asciicodes", action="store_const", const="True", help="Pattern as list of hex ascii codes")
    parser.add_argument("pattern", metavar="PATTERN", help="Pattern to search")
    parser.add_argument("file", metavar="FILE", help="File to search")
    # test_list = ["--asciicodes", "1F 8B 08", "file1.dat"]
    # test_list = ["AAAAA", "file2.dat"]
    # test_list = ["--asciicodes", "1F 8B 08", "file3.dat"]
    # args = parser.parse_args(test_list)
    args = parser.parse_args()

    pattern = bytes()
    if args.asciicodes:
        # args.pattern = convert_to_str(args.pattern)
        pattern = bytes.fromhex(args.pattern)
    else:
        # convert string to bytes object
        pattern = bytes(args.pattern, "latin_1", "strict")

    
    # dump_bytes(args.pattern, 0, len(args.pattern))

    delta = 7
    p = 0
    with open(args.file, "rb") as f_in:
        s = f_in.read()
    r = s.find(pattern, p)
    while r > -1:
        f = max(1, r - delta)
        t = r + len(args.pattern) + delta
        if t > len(s):
            t = len(s)
        dump_bytes(s, f, t-f, 200)
        p = r + 1
        r = s.find(pattern, p)


if __name__ == "__main__":
    main()

