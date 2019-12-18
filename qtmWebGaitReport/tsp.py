# -*- coding: utf-8 -*-

import qtools
from os import path
import numpy as np
import c3dValidation
from pyCGM2.Lib import analysis

# workingDirectory = "E:\\OneDrive\\qualisys.se\\App Team - Documents\\Projects\\Gait web reports from Vicon c3d data\\Python parser\\Data\\Oxford\\"


class TSP:
    def __init__(self, workingDirectory):
        self.workingDirectory = workingDirectory
        self.null = None

        c3dValObj = c3dValidation.c3dValidation(workingDirectory)
        self.measurementNames = c3dValObj.getValidC3dList(True)
        self.fileNames = c3dValObj.getValidC3dList(False)
        self.perFilePyCGM2tspStats = {path.basename(name).replace(".c3d", ""): analysis.makeAnalysis(
            workingDirectory + "\\", [path.basename(name)]).stpStats for name in self.fileNames}

    def stepTime(self, side):
        # stepTimes = self.getParamFromPyCGM2("stepTime", [side])
        # returns an empty list since the stepTime is not implemented in the pyCGM2 analysis
        return []

    @staticmethod
    def calculateDoubleLimbSupportInSeconds(duration, percentage):
        params = []
        assert len(duration) == len(percentage), "duration and percantage inputs need to be of same length, but currently are len(duration)={} and len(percentage)={}".format(
            len(duration), len(percentage))
        for curDurations, curPercentages in zip(duration, percentage):
            measurementName = curDurations["measurement"]
            vals = np.array(curDurations["values"]) * \
                np.array(curPercentages["values"])/100
            params.append({"measurement": measurementName,
                           "values": vals.tolist()})
        return params

    def doubleLimbSupport(self, side):
        duration = self.getParamFromPyCGM2("duration", [side])
        doubleStancePercentage = self.getParamFromPyCGM2(
            "doubleStance1", [side])
        doubleStanceSeconds = TSP.calculateDoubleLimbSupportInSeconds(
            duration, doubleStancePercentage)
        return doubleStanceSeconds

    def strideTime(self):
        leftStrideTime = dict()
        rightStrideTime = dict()

        for filename in self.fileNames:
            acq = qtools.fileOpen(filename)
            measurementName = path.basename(filename)
            measurementName = measurementName.replace('.c3d', '')
            events = qtools.groupEvents(acq, measurementName, "time")

            leftStrideTime[measurementName] = qtools.timeBetweenEvents(
                measurementName, events, "LHS", "LHS")
            rightStrideTime[measurementName] = qtools.timeBetweenEvents(
                measurementName, events, "RHS", "RHS")

        return (leftStrideTime, rightStrideTime)

    def stanceTimePct(self, side):
        stanceTimePct = self.getParamFromPyCGM2("stancePhase", [side])
        return stanceTimePct

    def cadence(self):
        cadence = self.getParamFromPyCGM2(
            "cadence", ["Left", "Right"])
        return cadence

    def strideLength(self):
        strideLength = self.getParamFromPyCGM2(
            "strideLength", ["Left", "Right"])
        return strideLength

    def strideWidth(self):
        strideWidths = self.getParamFromPyCGM2(
            "strideWidth", ["Left", "Right"])
        return strideWidths

    def stepLength(self, side):
        stepLengths = self.getParamFromPyCGM2("stepLength", [side])
        return stepLengths

    @staticmethod
    def check_sides_validity(sides):
        acceptedSides = ["Left", "Right"]
        for side in sides:
            assert side in acceptedSides, "attribute side = {} needs to be in {}".format(
                side, acceptedSides)

    def getParamFromPyCGM2(self, parameterName, sides):
        TSP.check_sides_validity(sides)
        params = []
        for filename in self.fileNames:
            measurementName = path.basename(filename).replace('.c3d', '')
            vals = []
            for side in sides:
                vals += self.perFilePyCGM2tspStats[measurementName][(
                    parameterName, side)]["values"].tolist()
            params.append({"measurement": measurementName,
                           "values": vals})
        return params

    def export(self):
        exp = [{"id": "Left_Step_Time",
                "set": "left",
                "type": "scalar",
                "data": self.stepTime("Left")},
               {"id": "Right_Step_Time",
                "set": "right",
                "type": "scalar",
                "data": self.stepTime("Right")},
               {"id": "Left_Initial_Double_Limb_Support_Time",
                "set": "left",
                "type": "scalar",
                "data":  self.doubleLimbSupport("Left")},
               {"id": "Right_Initial_Double_Limb_Support_Time",
                "set": "right",
                "type": "scalar",
                "data":  self.doubleLimbSupport("Right")},
               {"id": "Left_Stance_Time_Pct",
                "set": "left",
                "type": "scalar",
                "data":  self.stanceTimePct("Left")},
               {"id": "Right_Stance_Time_Pct",
                "set": "right",
                "type": "scalar",
                "data":  self.stanceTimePct("Right")},
               {"id": "Cadence",
                "set": self.null,
                "type": "scalar",
                "data":  self.cadence()},
               {"id": "Stride_Length",
                "set": self.null,
                "type": "scalar",
                "data": self.strideLength()},
               {"id": "Stride_Width",
                "set": self.null,
                "type": "scalar",
                "data":  self.strideWidth()},
               {"id": "Left_Step_Length",
                "set": "left",
                "type": "scalar",
                "data":  self.stepLength("Left")},
               {"id": "Right_Step_Length",
                "set": "right",
                "type": "scalar",
                "data":  self.stepLength("Right")},

               ]
        return exp

# a = TSP(workingDirectory)
# b = a.strideLength()
# print b
