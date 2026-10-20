
from random import uniform
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window

Window.clearcolor = (0.035, 0.04, 0.08, 1)


class AimTrainer(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.targets = []
        self.spawn_targets()
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_interval(self.move_targets, 1 / 30)

    def spawn_targets(self):
        self.targets = [
            [uniform(.15, .85), uniform(.2, .8),
             uniform(-.003, .003), uniform(-.003, .003)]
            for _ in range(5)
        ]
        self.draw()

    def move_targets(self, dt):
        for t in self.targets:
            t[0] += t[2]
            t[1] += t[3]
            if not .1 < t[0] < .9:
                t[2] *= -1
            if not .15 < t[1] < .85:
                t[3] *= -1
        self.draw()

    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(.04, .05, .1, 1)
            Rectangle(pos=self.pos, size=self.size)
            for x, y, dx, dy in self.targets:
                cx = self.x + x * self.width
                cy = self.y + y * self.height
                s = min(self.width, self.height) * .08
                Color(.7, .25, 1, 1)
                Line(rectangle=(cx-s/2, cy-s/2, s, s), width=2)
                Color(.2, 1, .7, 1)
                Line(points=[cx-s/4, cy, cx+s/4, cy], width=2)
                Line(points=[cx, cy-s/4, cx, cy+s/4], width=2)

    def on_touch_down(self, touch):
        for t in self.targets:
            cx = self.x + t[0] * self.width
            cy = self.y + t[1] * self.height
            if abs(touch.x-cx) < self.width*.06 and abs(touch.y-cy) < self.height*.08:
                self.score += 1
                self.targets.remove(t)
                self.targets.append([
                    uniform(.15, .85), uniform(.2, .8),
                    uniform(-.003, .003), uniform(-.003, .003)
                ])
                app = App.get_running_app()
                app.score.text = "SCORE: " + str(self.score)
                self.draw()
                return True
        return super().on_touch_down(touch)


class BladeXX(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=8)
        root.add_widget(Label(
            text="[b]BLADEXX[/b]", markup=True,
            font_size="32sp", color=(.72, .35, 1, 1),
            size_hint_y=.14
        ))
        root.add_widget(Label(
            text="AIM TRAINER  •  ESP DEMO",
            color=(.2, 1, .7, 1), size_hint_y=.08
        ))
        self.score = Label(text="SCORE: 0", size_hint_y=.08)
        root.add_widget(self.score)
        field = AimTrainer()
        root.add_widget(field)
        reset = Button(
            text="НОВЫЙ РАУНД", size_hint_y=.12,
            background_normal="",
            background_color=(.42, .12, .72, 1)
        )
        reset.bind(on_release=lambda *_: self.reset(field))
        root.add_widget(reset)
        return root

    def reset(self, field):
        field.score = 0
        self.score.text = "SCORE: 0"
        field.spawn_targets()


if __name__ == "__main__":
    BladeXX().run()

