import operator
import sys


class Utils:
    @staticmethod
    def sortListOfObj(listOfObjToSort: list, attribute: str, ascending: bool):
        listOfObjToSort.sort(key=lambda x: x[attribute], reverse=(not ascending))


class ProgramManager:
    @staticmethod
    def isVenvOn():
        prefix = getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix
        return prefix != sys.prefix
