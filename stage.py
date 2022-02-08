from track import Track
import random
import numpy as np

class Stage:
    """
        场景逻辑类
    """
    def __init__(self):
        self.tracks = []
        self.width = 720
        self.height = 540
        self.g = 98 # 重力加速度参数
        self.dt = 0.05 # 时间间隔

    def addFireWork(self):
        """
            生成新的烟花
        """
        pos = [random.random() * self.width, self.height + 20]
        velocity = [40 - 80 * random.random(), -200 - 120 * random.random()]
        explodeThreshold = 2.2 + 0.2 * random.random()
        newFireWork = Track(pos=pos, velocity=velocity, explodeThreshold=explodeThreshold, alphaDelayRate=100, color=[255, 255, 255])
        self.tracks.append(newFireWork)

    def motionUpdate(self, eachTrack):
        """
            运动状态的更新
        """
        # 考虑空气阻力、重力
        eachTrack.pos[0] = eachTrack.pos[0] + eachTrack.velocity[0] * self.dt
        eachTrack.pos[1] = eachTrack.pos[1] + eachTrack.velocity[1] * self.dt
        v = (eachTrack.velocity[0]**2 + eachTrack.velocity[1]**2)**0.5
        vx = eachTrack.velocity[0]
        vy = eachTrack.velocity[1]
        eachTrack.velocity[0] = vx - eachTrack.gamma * v * vx * self.dt
        eachTrack.velocity[1] = vy + (self.g - eachTrack.gamma * v * vy) * self.dt

    def alphaUpdate(self, eachTrack, p):
        """
            alpha的更新
        """
        newAlpha = p.alpha - eachTrack.alphaDelayRate * self.dt
        p.alpha = newAlpha if newAlpha >= 0 else 0

    def explosionWillow(self, eachTrack, newTrackList):
        """
            炸出柳树烟花
        """
        color = [255 * random.random(), 255 * random.random(), 255 * random.random()]
        alphaDelayRate = 100
        velocityAmp = 60 + 40 * random.random()
        # 爆炸，放出烟花轨迹
        for theta in np.linspace(0, 2*np.pi, int(4 + 6 * random.random())+1, endpoint=False):
            theta += 15 / 180 * np.pi - 30 / 180 * np.pi * random.random()
            pos = [eachTrack.pos[0], eachTrack.pos[1]]
            velocity = np.array([velocityAmp * np.cos(theta), velocityAmp * np.sin(theta)]) + np.array(eachTrack.velocity)
            newTrack = Track(pos=pos, velocity=velocity, explodeThreshold=np.inf, alphaDelayRate=alphaDelayRate, color=color, gamma=1e-2)
            newTrackList.append(newTrack)

    def explosionPeacock(self, eachTrack, newTrackList):
        """
            孔雀开屏
        """
        alphaDelayRate = 255
        for theta in np.linspace(0, 2*np.pi, 30, endpoint=False):
            velocityAmp = 40 + 80 * random.random()
            color = [255 * random.random(), 255 * random.random(), 255 * random.random()]
            pos = [eachTrack.pos[0], eachTrack.pos[1]]
            velocity = np.array([velocityAmp * np.cos(theta), velocityAmp * np.sin(theta)]) + np.array(eachTrack.velocity)
            newTrack = Track(pos=pos, velocity=velocity, explodeThreshold=np.inf, alphaDelayRate=alphaDelayRate, color=color, gamma=1e-2)
            newTrack.maxNodeNumber = 3
            newTrackList.append(newTrack)

    def doubleExplosion(self, eachTrack, newTrackList):
        """
            二级爆炸
        """
        color = [255, 255, 255]
        alphaDelayRate = 200
        velocityAmp = 160 + 20 * random.random()
        # 爆炸，放出烟花轨迹
        for theta in np.linspace(0, 2*np.pi, int(5 + 2 * random.random())+1, endpoint=False):
            theta += 15 / 180 * np.pi - 30 / 180 * np.pi * random.random()
            pos = [eachTrack.pos[0], eachTrack.pos[1]]
            velocity = np.array([velocityAmp * np.cos(theta), velocityAmp * np.sin(theta)]) + np.array(eachTrack.velocity)
            newTrack = Track(pos=pos, velocity=velocity, explodeThreshold=1, alphaDelayRate=alphaDelayRate, color=color, gamma=1e-2)
            newTrackList.append(newTrack)

    def explosionStateUpdate(self, eachTrack, newTrackList):
        """
            更新爆炸状态
        """
        eachTrack.lifeTime += self.dt
        if (eachTrack.lifeTime - self.dt < eachTrack.explodeThreshold <= eachTrack.lifeTime):
            eachTrack.isExplode = True
            fireWorkType = int(3 * random.random())
            if(fireWorkType == 0):
                self.explosionWillow(eachTrack, newTrackList)
            elif(fireWorkType == 1):
                self.explosionPeacock(eachTrack, newTrackList)
            elif(fireWorkType == 2):
                if(len(self.tracks) <= 255):
                    self.doubleExplosion(eachTrack, newTrackList)
                else:
                    self.explosionWillow(eachTrack, newTrackList)

    def trackListUpdate(self, newTrackList, deleteTrackList):
        """
            增加/删除track
        """
        # 增加新的轨迹
        for eachNewTrackList in newTrackList:
            self.tracks.append(eachNewTrackList)
        # 移除结点全部删光了的链表（以及跑出屏幕一定距离的）
        for eachTrack in self.tracks:
            if(eachTrack.nodeNumber == 0):
                deleteTrackList.append(eachTrack)
            if(((eachTrack.pos[0] - self.width / 2)**2 + (eachTrack.pos[1] - self.height / 2)**2)**0.5 >= 500):
                deleteTrackList.append(eachTrack)
        for eachDeleteTrackList in deleteTrackList:
            self.tracks.remove(eachDeleteTrackList)

    def unExplosionTrackUpdate(self, eachTrack):
        """
            未爆炸track的更新
        """
        p = eachTrack.head.last
        # 结点数未达上限时，新增到链表末尾
        if(eachTrack.nodeNumber < eachTrack.maxNodeNumber):
            eachTrack.addNode(p.pos, 255, p.color)
        # 头结点位置、速度更新
        self.motionUpdate(eachTrack)
        # 各个结点的位置、alpha更新
        while(p != eachTrack.head):
            p.pos = p.last.pos
            self.alphaUpdate(eachTrack, p)
            p = p.last
        # 头结点：
        p.pos = [eachTrack.pos[0], eachTrack.pos[1]]
        self.alphaUpdate(eachTrack, p)

    def explosionTrackUpdate(self, eachTrack):
        """
            爆炸track的更新
        """
        # 所有结点往头结点方向移动一位
        p = eachTrack.head.last
        while(p != eachTrack.head):
            p.pos = p.last.pos
            p.alpha = p.last.alpha
            p = p.last
        eachTrack.delNode(p)
        # 如果已经删的只剩头了，就可以消失了
        if(eachTrack.nodeNumber == 1):
            eachTrack.nodeNumber = 0

    def stateUpdate(self):
        """
            烟花状态更新
        """
        newTrackList = []
        deleteTrackList = []
        for eachTrack in self.tracks:
            # 未爆炸情形
            if(eachTrack.isExplode == False):
                self.unExplosionTrackUpdate(eachTrack)
            # 爆炸情形：对于已经爆炸了的火药，自然是不能留了，现在所能看到的是视觉残留
            else:
                self.explosionTrackUpdate(eachTrack)
            # 更新爆炸状态
            self.explosionStateUpdate(eachTrack, newTrackList)
        # 增加/删除track
        self.trackListUpdate(newTrackList, deleteTrackList)
