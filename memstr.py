# Available under MIT license. Check README.md for help.
# Dimitris Karagkasidis, https://github.com/pageflt

import gdb
import re

class memstr(gdb.Command):
    """Generate arbitrary strings out of ELF binary's contents"""

    def __init__(self):
        # Register new command with GDB
        super(memstr, self).__init__("memstr",
                                     gdb.COMMAND_NONE,
                                     gdb.COMPLETE_NONE)


    def invoke(self, args, from_tty):
        sections = {}
        target_string = []

        # Parse command arguments
        argv = gdb.string_to_argv(args)
        if len(argv) != 2:
            raise gdb.GdbError("Usage: memstr STRING SECTIONS")

        # Extract the address ranges of sections to be searched
        search_sections = argv[1].split(",")
        for entry in gdb.execute("info files", False, True).split("\n"):
            entry = entry.strip()
            if entry.startswith("0x"):
                for section in search_sections:
                    if entry.endswith(section):
                        r = re.search( "(0x.*) - (0x.*) is .*$", entry)
                        sections[section] = [r.group(1), r.group(2)]

        # Search for target characters in specified sections
        for char in argv[0]:
            found = False
            for section in sections:
                search_cmd = "find /b %s,%s,%s" % (sections[section][0],
                                                   sections[section][1],
                                                   hex(ord(char)))
                for r in gdb.execute(search_cmd, False, True).split("\n"):
                    if r.startswith("0x"):
                        r = r.split(" ")[0]
                        target_string.append((char, r))
                        found = True
                        break

                if found: break

        # Find a NULL byte to terminate the generated string
        for section in sections:
            search_cmd = "find /b %s,%s,0x00" % (sections[section][0],
                                                 sections[section][1])
            for r in gdb.execute(search_cmd, False, True).split("\n"):
                if r.startswith("0x"):
                    r = r.split(" ")[0]
                    target_string.append(("\\0", r))
                    break

        # If successful, display the resulting string as a Python list
        if len(argv[0]) == len(target_string) - 1:
            print self.generate_code(target_string)
        else:
            print "Could not generate the specified string from specified sections' contents"


    def generate_code(self, target_string):
        # Display the resulting string as addresses in a Python list.
        
        # ...A sloppy way to detect architecture. This works only for
        # x86 and x86-64 architectures for the time being (little-endian)
        pack_fmt = "<I"
        arch = gdb.execute("show architecture", False, True)
        if arch.find("x86-64") != -1:
            pack_fmt = "<Q"

        # Build the Python list of memory addresses for each character
        code = "STR = [\n"
        for t in target_string[:-1]:
            code += "\tstruct.pack('%s', %s),\t# %c\n" % (pack_fmt, t[1], t[0]) 
        code += "\tstruct.pack('%s', %s)\t# \\0\n]\n" % (pack_fmt, target_string[-1][1])
        return code


# Create an instance of memstr command
memstr()
