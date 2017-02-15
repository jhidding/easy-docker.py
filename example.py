#!/usr/bin/env python3

from archive import (Archive)
from easy_docker import (DockerContainer)

sed_program = """# usage: sed -f rot13.sed
y/abcdefghijklmnopqrstuvwxyz/nopqrstuvwxyzabcdefghijklm/
y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/NOPQRSTUVWXYZABCDEFGHIJKLM/
"""

message = "Vf gurer nalobql BHG gurer?"

with DockerContainer('busybox') as c:
    c.put_archive(
        Archive('w')
        .add_text_file('rot13.sed', sed_program)
        .add_text_file('input.txt', message)
        .close())

    c.run([
        '/bin/sh', '-c',
        "/bin/sed -f 'rot13.sed' < input.txt > output.txt"])

    secret = c.get_archive('output.txt').get_text_file('output.txt')

    print(secret)
