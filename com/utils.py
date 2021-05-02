import operator


class Utils:
    @staticmethod
    def sortListOfObj(listOfObjToSort: list, attribute: str, ascending: bool):
        listOfObjToSort.sort(key=lambda x: x[attribute], reverse=(not ascending))
