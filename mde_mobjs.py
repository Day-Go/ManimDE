from manim import *
from colour import Color

class MobjectConfig:
    def __init__(self) -> None:
        self.scene = None
        self.kwargs = None
        self.scaling_factor = 1

class MobjectDE:
    cfg = MobjectConfig()

    def __init__(self) -> None:
        self.buffer = []

        # Value
        self.value = DecimalNumber(0, num_decimal_places=0, edge_to_fix=LEFT)
        self.value.font_size = DEFAULT_FONT_SIZE * self.cfg.scaling_factor
        self.v_tracker = ValueTracker(0)
        self.value.add_updater(
            lambda n: n.set_value(self.v_tracker.get_value())
        )
        self.value.add_updater(
            lambda n: n.move_to(VMobject().set_points(self.points).get_center())
        )

        # Index
        self.index = DecimalNumber(0, num_decimal_places=0, edge_to_fix=LEFT)
        self.index.font_size = DEFAULT_FONT_SIZE * self.cfg.scaling_factor
        self.i_tracker = ValueTracker(0)
        self.index.add_updater(
            lambda i: i.set_value(self.i_tracker.get_value())
        )

        self.index.add_updater(
            lambda i: i.move_to(
                VMobject().set_points(self.points).get_top() + [0, self.height/6, 0]
            )
        )

        self.add(self.value)
        self.add(self.index)     

    def __gt__(self, other: Mobject) -> bool:
        result = self.val > other.val

        if result:
            pass
        else:
            pass

        return result 

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        if SquareDE.cfg.scene:
            SquareDE.cfg.scene.play(
                self.v_tracker.animate.set_value(new_val),
                run_time=0.2
            )
        else:
            self.v_tracker.set_value(new_val)

        self._val = new_val

    @val.getter
    def val(self):
        return self._val

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, new_idx):
        if SquareDE.cfg.scene:
            SquareDE.cfg.scene.play(
                self.i_tracker.animate.set_value(new_idx),
                run_time=0.05
            )
        else:
            self.i_tracker.set_value(new_idx)

        self._idx = new_idx

    @idx.getter
    def idx(self):
        return self._idx



class SquareDE(Square, MobjectDE):
    def __init__(self, side_length: int = 2, **kwargs):
        print(f'Initializing square with width = {self.cfg.scaling_factor}')
        super().__init__(side_length * self.cfg.scaling_factor, **self.cfg.kwargs)
        MobjectDE.__init__(self)


class CircleDE(Circle, MobjectDE):
    def __init__(self, radius: float | None = 1, color: Color | str = WHITE, **kwargs):
        super().__init__(radius, color, **self.cfg.kwargs)
        MobjectDE.__init__(self)
        