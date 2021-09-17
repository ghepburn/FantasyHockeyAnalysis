import sys

from FantasyHockeyController import FantasyHockeyController

cmdLineArguments = sys.argv
cmdLineArguments = cmdLineArguments[1:]

parameters = {}
for arg in cmdLineArguments:
    argList = arg.split("=")
    key=argList[0]
    value=argList[1]
    parameters[key] = value

controller = FantasyHockeyController(**parameters)

controller.buildCsv()