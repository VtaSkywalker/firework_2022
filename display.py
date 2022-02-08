import pygame
import sys
from stage import Stage

class Display:
    """
        画面显示
    """
    def __init__(self):
        self.stage = Stage()
        pygame.init()
        self.size = (self.stage.width, self.stage.height)
        self.screen = pygame.display.set_mode(self.size)

    def mainLoop(self):
        FRAME_INTERV = 17
        FIREWORK_INTERV = 0.33
        TIME_SCALE = 2
        tick = 0
        fireWorkTick = 0
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    sys.exit()
            pygame.time.delay(FRAME_INTERV)
            tick += 1
            fireWorkTick += 1
            if(tick == round(self.stage.dt / (FRAME_INTERV / 1e3) / TIME_SCALE)):
                # print(self.stage.tracks)
                self.stage.stateUpdate()
                tick = 0
            if(fireWorkTick == round(FIREWORK_INTERV / (FRAME_INTERV / 1e3) / TIME_SCALE)):
                self.stage.addFireWork()
                fireWorkTick = 0
            self.draw()
            pygame.display.update()

    def draw(self):
        """
            绘制烟花
        """
        self.screen.fill((0,0,0))
        for eachTrack in self.stage.tracks:
            p = eachTrack.head
            while(p.next != eachTrack.head):
                surface = pygame.Surface((5,5), pygame.SRCALPHA)
                color = [p.color[0], p.color[1], p.color[2], p.alpha]
                pygame.draw.circle(surface, color=color, center=(2.5,2.5), radius=2.5, width=0)
                self.screen.blit(surface, (p.pos[0], p.pos[1]))
                p = p.next
