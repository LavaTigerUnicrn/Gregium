"""
More of a proof on concept, use at your own risk
"""

import math
import struct
import sys
import urllib.request
from collections.abc import Sequence
from http.client import HTTPResponse
from io import BytesIO

import pygame
from PIL import Image as PIL_Image

halfPi = math.pi / 2
pi = math.pi
brightness_map: str = (
    " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
)
brightness_map_divisor: float = round(255 / (len(brightness_map) - 1), 5)
brightness_map_mean_divisor: float = round(255 / (len(brightness_map) - 1), 5) * 3


def getDirFromPos(y: int, x: int, half_width: float, half_height: float):
    """
    Gets the angle in radians of x,y centered about half_width,half_height
    """
    if x == half_width:
        return halfPi + (pi if y - half_height < 0 else 0)
    return math.atan((y - half_height) / (x - half_width)) + (
        pi if x - half_width < 0 else 0
    )


def getPosFromAngle(angle: float, distance: float) -> tuple[float, float]:
    """
    Angle should be in radians
    """
    return (distance * math.cos(angle), distance * math.sin(angle))


def colorPixel(pixel: tuple[int, int, int, int]) -> tuple[str, str]:
    """
    Returns the correct pixel with color

    Arguments:
        pixel:
            Color using r,g,b,a values
    """

    alpha = pixel[3]
    r = min(pixel[0], alpha)
    g = min(pixel[1], alpha)
    b = min(pixel[2], alpha)
    symbol = brightness_map[
        min(max(math.ceil((r + g + b) / brightness_map_mean_divisor), 0), 91)
    ]

    if symbol == " ":
        return (" ", " ")
    return (f"\x1b[38;2;{r};{g};{b}m{symbol}", symbol)


def compilePixelData(data: list[list[tuple[int, int, int, int]]]) -> str:
    """
    Returns compiled string based on pixel data
    """
    str_dat = []

    prev_px = (0, 0, 0, 0)
    prev_px_str = " "

    for row in data:
        for pixel in row:

            if prev_px == pixel:

                str_dat.append(prev_px_str)

                continue

            prev_px = pixel

            px, prev_px_str = colorPixel(pixel)
            str_dat.append(px)
        str_dat.append("\n")

    return "".join(str_dat)


def averageTuplesWeighted(
    tuple1: Sequence[float], tuple2: Sequence[float], weight1: float, weight2: float
) -> tuple:
    return tuple(
        [
            (
                int((tuple1[i] * weight1 + tuple2[i] * weight2) / 2)
                if i < 3
                else min(tuple1[i] + tuple2[i], 255)
            )
            for i in range(len(tuple1))
        ]
    )


class Surface:
    width: int
    height: int
    alpha: int

    def __init__(
        self,
        width: int,
        height: int,
        forceNoData: bool = False,
    ):
        """
        Generates a new surface that is able to be blitted to another or viewed with __str__

        Arguments:
            width:
                The width of the surface
            height:
                The height of the surface
            forceNoData:
                Generates the surface blank if true (data must be added manually)

                This will still generate alpha pixels when applicable
        """
        self.width: int = width
        self.height: int = height
        self.alpha: int = 1

        if not forceNoData:
            self.data: list[list[tuple[int, int, int, int]]] = [
                [(0, 0, 0, 255) for w in range(width)] for h in range(height)
            ]

    def set_alpha(self, value: int):
        """
        Sets the alpha override (0-1)
        THIS IS NOT THE SAME AS PIXEL ALPHA VALUE
        """
        self.alpha = value

    def blit(self, surface: "Surface", coordinates: tuple[int, int]):
        """
        Copies all pixels to the given surface

        To blit faster while ignoring alpha blending use blit_no_alpha()
        """

        # Get important values
        surface_width = surface.width
        surface_height = surface.height
        data = self.data
        width = self.width
        height = self.height
        surface_data = surface.data
        x_modif = int(coordinates[0])
        y_modif = int(coordinates[1])
        alpha = surface.alpha * 2  # Multiplied by 2 for averageTuplesWeighted function

        # Cancel if the surface has no alpha
        if alpha == 0:
            return
        for y in range(surface_height):

            # Stop if out of y bounds
            if y + y_modif >= height:
                return

            # Load row data
            surface_data_row = surface_data[y]
            data_row = data[y + y_modif]

            for x in range(surface_width):

                # End current line if out of x bounds
                if x + x_modif >= width:
                    break

                # Get data at the position
                data_pos = surface_data_row[x]

                # Get alpha
                alphaModif = alpha * (data_pos[3] / 255)

                # Merge colors
                data_row[x + x_modif] = averageTuplesWeighted(
                    data_pos,
                    data_row[x + x_modif],
                    alphaModif,
                    2 - alphaModif,
                )

    def blit_no_blend(self, surface: "Surface", coordinates: tuple[int, int]):
        """
        Copies all pixels to the given surface whilst ignoring alpha

        **THIS WILL STILL COPY ALPHA OF PIXELS**

        Should be decently faster
        """

        # Get important values
        surface_width = surface.width
        surface_height = surface.height
        data = self.data
        width = self.width
        height = self.height
        surface_data = surface.data
        x_modif = int(coordinates[0])
        y_modif = int(coordinates[1])

        for y in range(surface_height):

            # Stop if out of y bounds
            if y + y_modif >= height:
                return

            # Load row data
            surface_data_row = surface_data[y]
            data_row = data[y + y_modif]

            for x in range(surface_width):

                # End current line if out of x bounds
                if x + x_modif >= width:
                    break

                # Update data at current position
                data_row[x + x_modif] = surface_data_row[x]

    def blit_center(self, surface: "Surface", coordinates: tuple[int, int]):
        self.blit(
            surface,
            (
                int(coordinates[0] - surface.width / 2),
                int(coordinates[1] - surface.height / 2),
            ),
        )

    def fill(self, color: tuple[int, int, int, int]):
        """
        Sets all pixels to a given color
        """
        data = self.data
        for y in range(self.height):
            for x in range(self.width):
                data[y][x] = color
        self.data = data

    def subsurface(self, left: int, right: int, top: int, bottom: int) -> "Surface":
        """
        Returns a subsurface of this surface

        Arguments:
            left: The leftmost pixel to include
            right: The rightmost pixel (this is shifted down by 1, like [left:right])
            top: The topmost pixel to include (which is the lowest value since the data stretches from top->bottom low->high)
            bottom: The bottommost pixel (this is shifted down by 1, like [top:bottom])
        """

        data = self.data
        new_surface = Surface(right - left, bottom - top, forceNoData=True)
        new_surface.data = [row[left:right] for row in data[top:bottom]]
        return new_surface

    def __str__(self):

        return compilePixelData(self.data)


WINDOW: Surface = Surface(0, 0)


class display:
    @staticmethod
    def set_mode(width: int, height: int):
        """
        Generate window
        """
        global WINDOW
        WINDOW = Surface(width, height)
        return WINDOW

    @staticmethod
    def write(ratio: float = 1):
        """
        Write data to terminal (Must call flip after)

        This does not work on CMD terminal, use `display.write_flip_safe()` instead

        Arguments:
            ratio:
                The ratio of width to height of each character (on most terminals is about 0.6)
        """
        sys.stdout.write("\x1b[H\x1b[2\x1b[3J\x1b[3J")
        if ratio == 1:
            sys.stdout.write(WINDOW.__str__())
        else:
            sys.stdout.write(
                transform.scale(
                    WINDOW, (WINDOW.width, int(WINDOW.height * ratio))
                ).__str__()
            )

    @staticmethod
    def flip():
        """
        Flush terminal (Must be called after write)
        """
        sys.stdout.flush()


class image:

    @staticmethod
    def load_pygame(surf: pygame.Surface) -> Surface:
        """
        Converts a pygame surface into ascii surface

        This needs to be flipped across the x and rotated 90 degrees in order to render properly

        Arguments:
            surf:
                The pygame surface
        """

        return image.from_bytes(
            pygame.image.tobytes(surf, "RGBA"),
            surf.size,
        )

    @staticmethod
    def load_web(url: str) -> Surface:
        """
        Loads an image from the web

        Arguments:
            url:
                The url to load from
        """
        response: HTTPResponse = urllib.request.urlopen(
            url
        )
        img = PIL_Image.open(BytesIO(response.read()))
        return image.load_pil(img)

    @staticmethod
    def load_pil(img: PIL_Image.Image) -> Surface:
        """
        Loads an image from a pillow image instance

        Arguments:
            img:
                The pillow image instance
        """

        width, height = img.width, img.height
        imag = img.convert("RGBA").load()
        if imag is None:
            return Surface(0, 0)
        surface = Surface(width, height, True)
        surface_data = []
        for y in range(height):
            line = []
            for x in range(width):
                line.append(imag[x, y])
            surface_data.append(line)
        surface.data = surface_data
        return surface

    @staticmethod
    def from_bytes(data: bytes, size: tuple[int, int]) -> Surface:
        """
        Loads an image to a surface directly from bytes

        Arguments:
            data:
                The bytes data of the image
            size:
                The size of the image (width,height)

        **THE IMAGE MUST BE IN RGBA FORMAT**
        """

        width, height = size

        x = 0

        surf_data = []

        line = []

        for pixel in struct.iter_unpack("4B", data):

            x += 1

            line.append(pixel)
            if x == width:

                x = 0

                surf_data.append(line)
                line = []

        surface = Surface(width, height, forceNoData=True)

        surface.data = surf_data

        return surface

    @staticmethod
    def load(path: str) -> Surface:
        """
        Loads an image from your drive

        Arguments:
            path:
                The path to the image
        """

        return image.load_pil(PIL_Image.open(path))


class transform:
    @staticmethod
    def scale(original: Surface, coordinates: tuple[int, int]) -> Surface:
        width = coordinates[0]
        height = coordinates[1]
        x_ratio = original.width / width
        y_ratio = original.height / height

        new = Surface(width, height, True)
        new_data = []
        data = original.data.copy()
        for y in range(height):
            row = []
            for x in range(width):
                row.append(data[int(y * y_ratio)][int(x * x_ratio)])
            new_data.append(row)

        new.data = new_data
        return new

    @staticmethod
    def scale_by(original: Surface, factor: float) -> Surface:

        return transform.scale(
            original, (int(original.width * factor), int(original.height * factor))
        )

    @staticmethod
    def rotate(original: Surface, angle_degree: float) -> Surface:
        angle_radian = math.radians(angle_degree)
        width = original.width
        height = original.height
        half_height = height / 2
        half_width = width / 2
        data = original.data

        new_width = 0
        new_height = 0

        a1 = getDirFromPos(height, width, half_width, half_height) - angle_radian
        a2 = getDirFromPos(0, width, half_width, half_height) - angle_radian
        a3 = getDirFromPos(0, 0, half_width, half_height) - angle_radian
        a4 = getDirFromPos(height, 0, half_width, half_height) - angle_radian

        radius = math.sqrt((height - half_height) ** 2 + (width - half_width) ** 2)
        x1, y1 = getPosFromAngle(a1, radius)
        x2, y2 = getPosFromAngle(a2, radius)
        x3, y3 = getPosFromAngle(a3, radius)
        x4, y4 = getPosFromAngle(a4, radius)

        min_x = min(x1, x2, x3, x4)
        min_y = min(y1, y2, y3, y4)
        max_x = max(x1, x2, x3, x4)
        max_y = max(y1, y2, y3, y4)

        new_width = math.ceil(max_x - min_x)
        new_height = math.ceil(max_y - min_y)

        new_half_width = new_width / 2
        new_half_height = new_height / 2
        new_surface = Surface(new_width, new_height, forceNoData=True)
        new_data = []

        for y in range(new_height):
            row = []
            for x in range(new_width):
                angle = getDirFromPos(
                    y, x, new_half_width, new_half_height
                )  # I LOVE A2T
                distance = math.sqrt(
                    (x - new_half_width) ** 2 + (y - new_half_height) ** 2
                )
                angle += angle_radian
                new_x, new_y = getPosFromAngle(angle, distance)
                new_x = int(new_x + half_width)
                new_y = int(new_y + half_height)

                if width - 1 < new_x or new_x < 0:
                    row.append((0, 0, 0, 0))
                    continue
                if height - 1 < new_y or new_y < 0:
                    row.append((0, 0, 0, 0))
                    continue
                row.append(data[new_y][new_x])
            new_data.append(row)
        new_surface.data = new_data
        return new_surface

    @staticmethod
    def auto_trim(original: Surface) -> Surface:
        width = original.width
        height = original.height
        data = original.data.copy()
        trim_l = width
        trim_r = 0
        trim_u = height
        trim_d = 0
        for y in range(height):
            for x in range(width):
                if data[y][x][3] == 0:
                    continue

                trim_l = min(trim_l, x - 1)
                trim_d = max(trim_d, y + 1)
                trim_r = max(trim_r, x + 1)
                trim_u = min(trim_u, y - 1)

        # Ensure none is below 0 (or above width/height)
        trim_l = max(trim_l, 0)
        trim_r = min(trim_r, width)
        trim_u = max(trim_u, 0)
        trim_d = min(trim_d, height)

        return original.subsurface(trim_l, trim_r, trim_u, trim_d)

    @staticmethod
    def grayscale(original: Surface) -> Surface:
        width = original.width
        height = original.height

        new = Surface(width, height, True)
        new_data = []
        for pixelRow in original.data.copy():
            row = []
            for pixel in pixelRow:
                row.append(
                    tuple(
                        [
                            sum(pixel[:-1]) / 3,
                        ]
                        * 3
                        + [
                            pixel[3],
                        ]
                    )
                )
            new_data.append(row)

        new.data = new_data
        return new
