#!/usr/bin/env python3

from archive import (Archive)
from easy_docker import (DockerContainer)

awk_program = """# usage: awk -f rot13.awk
BEGIN {
  for(i=0; i < 256; i++) {
    amap[sprintf("%c", i)] = i
  }
  for(l=amap["a"]; l <= amap["z"]; l++) {
    rot13[l] = sprintf("%c", (((l-amap["a"])+13) % 26 ) + amap["a"])
  }
  FS = ""
}
{
  o = ""
  for(i=1; i <= NF; i++) {
    if ( amap[tolower($i)] in rot13 ) {
      c = rot13[amap[tolower($i)]]
      if ( tolower($i) != $i ) c = toupper(c)
      o = o c
    } else {
      o = o $i
    }
  }
  print o
}"""

message = "Vf gurer nalobql BHG gurer?"

with DockerContainer('busybox') as c:
    c.put_archive(
        Archive('w')
        .add_text_file('rot13.awk', awk_program)
        .add_text_file('input.txt', message)
        .close())

    c.run([
        '/bin/sh', '-c',
        "/bin/awk -f 'rot13.awk' < input.txt > output.txt"])

    secret = c.get_archive('output.txt').get_text_file('output.txt')

    print(secret)
