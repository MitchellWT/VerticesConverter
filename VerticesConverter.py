import json
from math import floor
from argparse import ArgumentParser

# Variables for output information
outputFileLocation = './convertedVertices.json'
outputIndentation = 4

class Main:
    __jsonFile = None
    __verticesList = None

    # Defines and sets command line argument variable
    def __init__(self):
        argumentParser = ArgumentParser(description='Convert vertices to zero\'d version.')
        argumentParser.add_argument('-j, --json',
                                    help='JSON file that contains vertices to be converted.',
                                    type=str,
                                    action='store',
                                    dest='json')

        args = argumentParser.parse_args()
        self.__jsonFile = vars(args)['json']

    # Validates in the input json and converts it into a list or dict's
    def validateAndLoadJSON(self):
        isValid = False

        try:
            with open(self.__jsonFile, 'r') as jsonFile:
                validJSON = json.load(jsonFile)
            
            self.__verticesList = validJSON['vertices']
        except:
            pass

        if self.__verticesList:
            isValid = True

        return isValid

    # Removes decimal places from vertices and zero's out values by subtracting
    # the lowest occuring value
    def convertVertices(self):
        localVerticesList = self.__verticesList
        lowestY = None
        lowestX = None

        for vertice in localVerticesList:
            vertice['x'] = floor(vertice['x'])
            vertice['y'] = floor(vertice['y'])

            if lowestX is None or vertice['x'] < lowestX:
                lowestX = vertice['x']
            if lowestY is None or vertice['y'] < lowestY:
                lowestY = vertice['y']

        for vertice in localVerticesList:
            vertice['x'] = vertice['x'] - lowestX
            vertice['y'] = vertice['y'] - lowestY

        self.__verticesList = localVerticesList
        return True

    # Saves vertices to JSON file
    def saveVerticesToFile(self):
        global outputFileLocation, outputIndentation

        saveComplete = False
        jsonStructure = {'vertices': self.__verticesList}

        try:
            with open(outputFileLocation, 'w') as outputFile:
                json.dump(jsonStructure, outputFile, indent=outputIndentation)
            
            saveComplete = True
        except:
            pass

        return saveComplete


if __name__ == '__main__':
    main = Main()
    
    if main.validateAndLoadJSON():
        if main.convertVertices():
            if main.saveVerticesToFile():
                print('COMPLETE: conversion complete and exported to \'' + outputFileLocation + '\'.')
            else:
                print('ERROR: unable to save vertices to file.')
        else:
            print('ERROR: unable to convert vertices.')
    else:
        print('ERROR: JSON is not in a valid format, view example JSON at https://github.com/MitchellWT.')