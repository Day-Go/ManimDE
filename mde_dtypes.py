from typing import Iterable
from manim import *
from mde_mobjs import SquareDE, CircleDE

class MobjectList(list):
    def __init__(self, seq: list = [], mobj_type: str = 'Square'):
        item_config = {
            'Circle': {
                'class': CircleDE,
                'kwargs': {
                    'radius': 1,
                    'color': RED
                }
            },
            'Square': {
                'class': SquareDE,
                'kwargs': {
                    'stroke_width': 4,
                    'color': WHITE
                }
            }
        }

        self.mobj_class = item_config[mobj_type]['class']
        self.mobj_class.cfg.kwargs = item_config[mobj_type]['kwargs']

        items = [self.mobj_class() for _ in range(len(seq))]

        for item, (idx, val) in zip(*[items, enumerate(seq)]):
            item.idx = idx
            item.val = val

        self.group = VGroup(*items).arrange(buff=0)
        
        super().__init__(items)

    def __repr__(self) -> str:
        return f'{[item.val for item in self]}'

    def init_scene(self, scene: Scene) -> None:
        self.scene = scene
        self.mobj_class.cfg.scene = scene
        self.render()

    def render(self) -> None:
        if self:
            self.scene.play(*[Create(mobj) for mobj in self])

    def __setitem__(self, idx: int, val: int | Mobject):
        if isinstance(val, int):
            self[idx].val = val

        elif isinstance(val, Mobject):
            self[idx].buffer.append(
                prepare_animation(self[idx].animate.move_to(val.get_center()))
            )

            super(MobjectList, self).__setitem__(idx, val)            

        self.execute_animation_buffer()

    def update_mobject_indicies(self) -> None:
        for idx, item in enumerate(self):
            item.idx = idx

    def scale_item_stroke_width(self) -> None:
        """
        Scale the stroke width of the mobjects in self.
        """
        for item in self:
            item.stroke_width = (
                DEFAULT_STROKE_WIDTH * 
                self.mobj_class.cfg.scaling_factor
            )

        self.mobj_class.cfg.kwargs['stroke_width'] = (
            DEFAULT_STROKE_WIDTH * self.mobj_class.cfg.scaling_factor
        )

    def scale_and_center_mobject_group(self) -> None:
        """
        
        """
        sf = 13 / self.group.width
        self.mobj_class.cfg.scaling_factor *= sf

        self.scene.play(
            self.group.animate.scale(sf).move_to(ORIGIN),
            run_time=0.5
        )


    def append(self, data: int) -> Iterable:
        mobject = self.mobj_class()
        mobject.idx = len(self)
        mobject.val = data
        mobject.next_to(
            VMobject().set_points(self.group[-1].points).get_right(), buff=0
        )

        self.group += mobject

        self.scene.play(FadeIn(mobject), run_time=0.5)

        items = super().append(mobject)

        self.scale_item_stroke_width()
        self.scale_and_center_mobject_group()
    
        return items

    def extend(self, __iterable: Iterable) -> Iterable:
        mobjects = [self.mobj_class() for _ in range(len(__iterable))]
            
        for mobject, (i, value) in zip(mobjects, enumerate(__iterable)):
            mobject.idx = len(self) + i
            mobject.val = value
            mobject.next_to(
                VMobject().set_points(self.group[-1].points).get_right(), 
                buff=0
            )

            self.group += mobject

        # self.scene.play(
        #     *[FadeIn(mobject) for mobject in mobjects],
        #     run_time=0.5
        # )

        items = super().extend(mobjects)

        self.scale_item_stroke_width()
        self.scale_and_center_mobject_group()

        return items

    def insert(self, __index: int, __data: int) -> None:
        mobject = self.mobj_class()
        mobject.idx = __index
        mobject.val = __data

        super().insert(__index, mobject)

        del self.group
        self.group = VGroup(*[item for item in self])
        self.group.arrange(RIGHT, buff=0)

        h_diff = (self.group.height - mobject.height) / 2

        mobject.shift(h_diff * DOWN)
        self.scene.play(FadeIn(mobject), run_time=0.5)

        self.scale_and_center_mobject_group()
        self.update_mobject_indicies()

    def remove(self, __value: int) -> None:
        values = [item.val for item in self]
        idx = values.index(__value)

        self.scene.play(FadeOut(self[idx]))
        self.scene.remove(self[idx])

        self.group -= self[idx]

        self.scene.play(
            self.group.animate.arrange(RIGHT, buff=0)
        )
        
        super().remove(self[idx])

        self.scale_and_center_mobject_group()
        self.update_mobject_indicies()

    def index(self, __value, __start: int = 0, __stop: int = None) -> int:
        if __stop is None:
            __stop = len(self)
        
        values = [item.val for item in self]

        idx = values.index(__value, __start, __stop)

        self[idx].set_z_index(100)
        self.scene.play(self[idx].animate.set(color=YELLOW))
        self.scene.play(self[idx].animate.set(color=WHITE), run_time=0.6)
        self[idx].set_z_index(0)
        return idx


    def execute_animation_buffer(self, s: slice = None) -> None:
        if s is None:
            s = self

        mobjects = []
        animations = []
        for item in s:
            if item.buffer:
                for ele in item.buffer:
                    if isinstance(ele, Transform) or isinstance(ele, Animation):
                        animations.append(ele)
                    elif isinstance(ele, Mobject):
                        mobjects.append(ele)

                item.buffer = []

        if animations:
            self.scene.play(*animations + [Create(mobj) for mobj in mobjects])
            self.update_mobject_indicies()

        if mobjects:
            self.scene.play(*[Uncreate(mobj) for mobj in mobjects])

        

class MobjectDict(dict):
    pass