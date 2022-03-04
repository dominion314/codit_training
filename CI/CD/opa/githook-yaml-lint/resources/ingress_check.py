"""
Script that runs ingress validation.
"""
import os
import sys

# generate walk of the filesystem in current directory
print("Beginning Check")
FILESYSTEM = os.walk(".")
CHECK_SUBDIRS = []

# boolean for exit code indicated an error when True
EXIT_CODE_BOOL = False

for root, dirnames, filenames in FILESYSTEM:
    # check if this directory has subdirs we are looking for
    # checks in list previously created
    if root in CHECK_SUBDIRS:
        CHECK_SUBDIRS.remove(root)
        if "check_uri" not in filenames \
                or "internal_dns" not in filenames \
                or "uris" not in filenames:
            print("Subdirectories are incorrect for: " + root)
            EXIT_CODE_BOOL = True
        else:
            # check length of check_uri and internal_dns
            if sum(1 for line in open(root + "/check_uri", "r+")) != 1:
                print("The check_uri file is not one line in " + root)
                EXIT_CODE_BOOL = True
            if sum(1 for line in open(root + "/internal_dns", "r+")) != 1:
                print("The internal_dns file is not one line in " + root)
                EXIT_CODE_BOOL = True

    # otherwise this is a new directory that may have domains
    if "domains" in filenames:
        domains_file = open(root + "/domains", "r+")
        domains = domains_file.readlines()
        for d in domains:
            if d.rstrip('\n') in dirnames:
                CHECK_SUBDIRS.append(os.path.join(root, d.rstrip('\n')))
            else:
                print("Not a Directory: " + root + "/" + d.rstrip('\n'))
                print("Check for empty line at end of domains file " + root + "/domains\n")
                EXIT_CODE_BOOL = True
        domains_file.close()
print("Completed")
sys.exit(EXIT_CODE_BOOL)
