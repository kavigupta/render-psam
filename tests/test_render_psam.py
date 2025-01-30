import unittest
from matplotlib import pyplot as plt
import numpy as np

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


class CreatePSAM(unittest.TestCase):
    def check(self, name):
        array_contents = matplotlib_to_array(plt.gcf())
        output_path = f"testing_output/{name}.png"
        if is_testing:
            expected_contents = plt.imread(output_path) * 255
            np.testing.assert_allclose(array_contents, expected_contents)
        else:
            plt.imsave(output_path, array_contents)

    def test_basic_normalized(self):
        psam = np.array(
            [
                [1, 0, 0, 0],
                [0, 2, 0, 0],
                [3, 0, 2, 0],
                [0, 1, 0, 1],
            ]
        )
        render_psam(psam, psam_mode="normalized")
        self.check("basic_normalized")
