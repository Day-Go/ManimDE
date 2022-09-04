from manim import Scene
import random
from mde_dtypes import MobjectList
from algos import *

class Demo(Scene):
    def construct(self) -> None:
        sequence = [random.randint(0,100) for _ in range(4)]

        data = MobjectList(sequence)
        data.init_scene(self)

        bubble_sort(data)

        for i in range(1,3):
            data.append(i * 3)
            data.insert(4, 666)
            data.extend([i*22, i*55])

        data.remove(666)

        self.wait()