class Track:
    """
        烟花的轨迹，由链表的形式存储
    """
    def __init__(self, pos, velocity, explodeThreshold, alphaDelayRate, color):
        self.pos = pos
        self.velocity = velocity
        self.head = TrackNode(pos, 255, color)
        self.head.next = self.head
        self.head.last = self.head
        self.nodeNumber = 1
        self.maxNodeNumber = 10
        self.lifeTime = 0
        self.isExplode = False
        self.explodeThreshold = explodeThreshold
        self.alphaDelayRate = alphaDelayRate

    def addNode(self, pos, alpha, color):
        """
            在尾部添加结点
        """
        p = self.head
        if(not p):
            return
        while(p.next != self.head):
            p = p.next
        newP = TrackNode(pos, alpha, color)
        p.next = newP
        newP.last = p
        newP.next = self.head
        self.head.last = newP
        self.nodeNumber += 1

    def delNode(self, dNode):
        """
            删除结点
        """
        p = self.head
        while(p != dNode):
            p = p.next
        if(p == self.head):
            self.head = p.next
        p.last.next = p.next
        p.next.last = p.last
        p.last = None
        p.next = None
        del p
        self.nodeNumber -= 1

class TrackNode:
    """
        烟花结点
    """
    def __init__(self, pos, alpha, color):
        self.pos = pos
        self.alpha = alpha
        self.color = color
        self.next = None
        self.last = None
