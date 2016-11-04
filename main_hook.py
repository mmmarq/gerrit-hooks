#!/usr/bin/env python
# .*. coding: UTF-8 .*.

from optparse import OptionParser
import sys

def main():
   usage = 'Usage: %prog --change <change id> --change-url <change url> --change-owner <change owner> --project <project name> --branch <branch> --topic <topic> --commit <sha1>'
   parser = OptionParser(usage)
   parser.set_defaults(keepSource=False)

   parser.add_option("--change", dest="change-id", help="Change Id")
   parser.add_option("--change-url", dest="change-url", help="Change URL")
   parser.add_option("--change-owner", dest="change-owner", help="Change Owner")
   parser.add_option("--project", dest="project-name", help="Project Name")
   parser.add_option("--branch", dest="branch-name", help="Branch Name")
   parser.add_option("--topic", dest="topic", help="Topic")
   parser.add_option("--commit", dest="commit", help="SHA1")

   (options, args) = parser.parse_args()

   print options
   sys.exit(0)

if __name__ == '__main__':
   main()

