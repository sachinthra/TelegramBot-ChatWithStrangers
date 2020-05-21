
class ManageUser:
    def __init__(self):
        self.dic = {}
        self.queue = []

    def newUser(self,item):
        if len(self.queue) == 0:
            self.queue.append(item)
            return -1 #wait
        else :
            match = self.queue.pop(0)
            if(match == item):
                if(len(self.queue) == 0):
                    self.queue.append(item)
                    return -1
                else:
                    match = self.queue.pop(0)
            
            self.addToDic(item,match)
            return match

    def addToDic(self,id1,id2):
        self.dic[id1] = id2
        self.dic[id2] = id1

    def delFromDic(self,id1,id2):
        del self.dic[id1]
        del self.dic[id2]
    def delOneFromQueue(self,id1):
        index = -1
        for i in self.queue:
            index+=1
            if id1 == i:
                break
        self.queue.pop(index)


    def isInDec(self,item):
        if item in self.dic:
            return self.dic[item]
        if item not in self.queue:
            return -2
        return -1


