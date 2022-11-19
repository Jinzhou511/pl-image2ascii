#!/usr/bin/env python

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter

from chris_plugin import chris_plugin, PathMapper
from PIL import Image

ascii_characters_by_surface = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
__version__ = '1.0.0'

DISPLAY_TITLE = r"""
       _   _                             _____                _ _ 
      | | (_)                           / __  \              (_|_)
 _ __ | |  _ _ __ ___   __ _  __ _  ___ `' / /' __ _ ___  ___ _ _ 
| '_ \| | | | '_ ` _ \ / _` |/ _` |/ _ \  / /  / _` / __|/ __| | |
| |_) | | | | | | | | | (_| | (_| |  __/./ /__| (_| \__ \ (__| | |
| .__/|_| |_|_| |_| |_|\__,_|\__, |\___|\_____/\__,_|___/\___|_|_|
| |   ______                  __/ |                               
|_|  |______|                |___/                                
"""


parser = ArgumentParser(description='A ChRIS plugin to convert RB image to ascii art',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-n', '--name', default='foo',
                    help='argument which sets example output file name')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')
parser.add_argument(
                        '--convert',
                        default     = '**/*jpg',
                        help        = '''Glob pattern to match all images to convert.'''
)


# fucntion part
def convert_to_ascii_art(inputfile: Path):
    #print("1")
    #print(inputfile)
    image = Image.open(inputfile)# Having issue
    
    #print(f"figure format: {image.format}")
    ascii_art = []
    (width, height) = image.size
    for y in range(0, height - 1):
        line = ''
        for x in range(0, width - 1):
            px = image.getpixel((x, y))
            line += convert_pixel_to_character(px)
        ascii_art.append(line)
    return ascii_art


def convert_pixel_to_character(pixel):
    (r, g, b) = pixel
    pixel_brightness = r + g + b
    max_brightness = 255 * 3
    brightness_weight = len(ascii_characters_by_surface) / max_brightness
    index = int(pixel_brightness * brightness_weight) - 1
    return ascii_characters_by_surface[index]


def save_as_text(ascii_art):
    with open("image.txt", "w") as file:
        for line in ascii_art:
            file.write(line)
            file.write('\n')
        file.close()


# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='imageto_ascii',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='2Gi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    """
    :param options: non-positional arguments parsed by the parser given to @chris_plugin
    :param inputdir: directory containing input files (read-only)
    :param outputdir: directory where to write output files
    """

    print(DISPLAY_TITLE)
    mapper = PathMapper.file_mapper(inputdir, outputdir,glob=options.convert)
    for input in mapper:
        #print(input)
        convert_to_ascii_art(input)
    output_file = outputdir / f'{options.name}.txt'
    output_file.write_text('did nothing successfully!')


if __name__ == '__main__':
    main()
