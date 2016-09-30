from subprocess import PIPE
from subprocess import Popen

# do the diff call + redirect stdout to output var
output = Popen(["diff","--unchanged-line-format=","--old-line-format=",
      "--new-line-format=%dn,", "exoplanet.eu_catalog.csv",
      "exoplanet.eu_catalog-2.csv"], stdout=PIPE)
# read from stdout
out = output.stdout.read()
out = out.split(',')[:-1]
# cast to int
out = list(map(int, out))
print(out)

if len(out) > 0:
    file = open("exoplanet.eu_catalog-2.csv")
    for i, line in enumerate(file):
        # header line
        if i == 0:
            print(line)
        if i in out:
            print(line)
        # note it's naturally sorted b/c of how diff works
        elif i > out[-1]:
            break