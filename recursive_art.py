""" TODO: Put your header comment here """

import random
import numpy as np
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth. Chooses functions from a list that includes
        product, average, cosine, and sine, nesting them appropriately
        based on min_depth and max_depth.

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
    """
    funcs = ['prod', 'avg', 'cos_pi', 'sin_pi', 'x', 'y']
    chosen_func = random.choice(funcs)
    if min_depth > 0:
        chosen_func = random.choice(funcs[0:4]) #if we haven't reached min_depth yet, we don't want to include x and y in the list of functions to choose from
    elif min_depth <= 0 and max_depth > 0:
        chosen_func = random.choice(funcs)
    elif max_depth == 0:
        chosen_func = random.choice(funcs[4:len(funcs)]) #if we've already reached max_depth, we don't want to continue; we only want to choose x or y

    if chosen_func == 'prod' or chosen_func == 'avg':
        return [chosen_func, build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)] #prod & avg each take 2 arguments
    elif chosen_func == 'cos_pi' or chosen_func == 'sin_pi':
        return [chosen_func, build_random_function(min_depth-1, max_depth-1)] #cos and sin take 1 argument each
    elif chosen_func == 'x' or chosen_func == 'y':
        return [chosen_func]



def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        f is the nested function representation outputted by build_random_function;
        it's a list from which we take everything needed to call evaluate_random_function

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == 'prod': #f[0] is the first part of the nested function, so it establishes the outermost function of the nest
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[1], x, y) #f[1] is another list: we take its first element...so on and so forth
    elif f[0] == 'avg':
        return 0.5 * (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[1], x, y))
    elif f[0] == 'cos_pi':
        return np.cos(np.pi * evaluate_random_function(f[1], x, y))
    elif f[0] == 'sin_pi':
        return np.sin(np.pi * evaluate_random_function(f[1], x, y))
    elif f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(3, 0, 4, 0, 20) #all the above tests are of the middle value; I want to make sure remap_interval works properly when val != the middle value of the input interval
        15.0
        >>> remap_interval(5, 4, 10, 0, 6) #this tests on the other side of the middle
        1.0
    """
    input_range = float(input_interval_end) - float(input_interval_start)
    output_range = float(output_interval_end) - float(output_interval_start)
    #we need to use the relationship b/w val and the input interval. This means making sure they stay mapped to each other
    val_relate = float(val) - float(input_interval_start)
    #val_relate / input_range = x (the variable we're evaluating) / output_range. This sets up the left side of that equation
    compare_ratio = float(val_relate) / float(input_range)
    #x is the number we want, mapped to 0. Adding this to output_interval_start will give us what we're really looking for
    x = float(output_range) * compare_ratio
    number = x + float(output_interval_start)
    return number


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart2.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
#    test_image("noise.png")