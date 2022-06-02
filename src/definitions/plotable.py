from random import randint
from typing import Tuple, List

Color = Tuple[int, int, int]

class ColorPanel (object):

    def __init__(self):
        pass

    @staticmethod
    def color(red: int, green: int, blue: int) -> Color:
        return (abs(red) % 255, abs(green) % 255, abs(blue) % 255)

    @staticmethod
    def random_color() -> Color:
        return ColorPanel.color(randint(0, 255), randint(0, 255), randint(0, 255))

    @staticmethod
    def color_diff(color1: Color, color2: Color) -> Color:
        return (color1[0] - color2[0],
                color1[1] - color2[1],
                color1[2] - color2[2])

    @staticmethod
    def increment_color(color: Color, inc: Color) -> Color:
        return ColorPanel.color(color[0] + inc[0],
                                color[1] + inc[1],
                                color[2] + inc[2]) 


    @staticmethod
    def color_grading(levels: int, base_color: Color, end_color: Color) -> List[Color]:
        diff = ColorPanel.color_diff(end_color, base_color)
        inc: Color = (diff[0] // levels, diff[1] // levels, diff[2] // levels)
    
        temp_color: Color = base_color
        res: List[Color] = [temp_color]
        for _ in range(levels):
            temp_color = ColorPanel.increment_color(temp_color, inc)
            res.append(temp_color)

        return res


# Abstraction of the fact that most of our objects will be able to be ploted in a graph
class Plotable (object):

    def __init__(self):
        pass    

    # method that will be overriden by each of our plotable objects
    def plot(self):
        pass

if __name__ == "__main__":
    cp = ColorPanel()
    print(cp.color_grading(10, (255,0,0), (0,0,0)))