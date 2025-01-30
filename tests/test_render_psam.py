import unittest

import numpy as np
from matplotlib import pyplot as plt
from parameterized import parameterized

from render_psam import render_psam

is_testing = True


def matplotlib_to_array(fig):
    """
    Convert a matplotlib figure to a numpy array
    """
    fig.canvas.draw()
    result = np.array(fig.canvas.renderer.buffer_rgba())
    plt.close(fig)
    return result


class CreatePSAMTests(unittest.TestCase):
    def check(self, name):
        array_contents = matplotlib_to_array(plt.gcf())
        output_path = f"testing_output/{name}.png"
        if is_testing:
            expected_contents = plt.imread(output_path) * 255
            assert (np.abs(array_contents - expected_contents) > 1).mean() < 0.01
        else:
            plt.imsave(output_path, array_contents)

    def ensure_is_testing(self):
        if not is_testing:
            raise ValueError("This test is not running in testing mode.")

    @parameterized.expand(
        [
            ("raw",),
            ("normalized",),
            ("info",),
        ]
    )
    def test_basic_mode(self, mode):
        psam = np.array(
            [
                [1, 0, 0, 0],
                [0, 2, 0, 0],
                [3, 0, 2, 0],
                [0, 1, 0, 1],
            ]
        )
        render_psam(psam, psam_mode=mode)
        self.check("basic_" + mode)
