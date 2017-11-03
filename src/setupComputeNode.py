# run this on the controller node
# must be in devstack/ directory
import subprocess
import sys
from helpers import admin


# can we use az names or just numbers?
def createAggregateZone(hostName, azName):
	ag = "-ag"
	agName = azName + ag
	admin()
	subprocess.call(["nova","aggregate-create", agName, azName])
	subprocess.call(["nova", "aggreagte-add-host", agName, hostName])
	subprocess.call(["nova", "availability-zone-list"])


def main():
	help = sys.argv[0] + " [compute-host-name]"
	if len(sys.argv) != 2:
		print(help)
	else:
		azName = "az-" + sys.argv[1] 
		createAggregateZone(sys.argv[1], azName)


if __name__ == "__main__":
	main()
