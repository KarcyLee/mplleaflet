#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from numpy.testing import assert_warns

from mplleaflet.mplexporter.exporter import Exporter
from mplleaflet.mplexporter.renderers import FakeRenderer, FullFakeRenderer
from matplotlib import pyplot as plt

import pytest


def fake_renderer_output(fig, Renderer):
    renderer = Renderer()
    exporter = Exporter(renderer)
    exporter.run(fig)
    return renderer.output


def _assert_output_equal(text1, text2):
    for line1, line2 in zip(text1.strip().split(), text2.strip().split()):
        assert line1 == line2


def test_lines():
    fig, ax = plt.subplots()
    ax.plot(range(20), '-k')

    _assert_output_equal(fake_renderer_output(fig, FakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw path with 20 vertices
                         closing axes
                         closing figure
                         """)

    _assert_output_equal(fake_renderer_output(fig, FullFakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw line with 20 points
                         closing axes
                         closing figure
                         """)


def test_markers():
    fig, ax = plt.subplots()
    ax.plot(range(2), 'ok')

    _assert_output_equal(fake_renderer_output(fig, FakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw path with 25 vertices
                         draw path with 25 vertices
                         closing axes
                         closing figure
                         """)

    _assert_output_equal(fake_renderer_output(fig, FullFakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw 2 markers
                         closing axes
                         closing figure
                         """)


def test_path_collection():
    fig, ax = plt.subplots()
    ax.scatter(range(3), range(3))

    _assert_output_equal(fake_renderer_output(fig, FakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw path with 25 vertices
                         draw path with 25 vertices
                         draw path with 25 vertices
                         closing axes
                         closing figure
                         """)

    _assert_output_equal(fake_renderer_output(fig, FullFakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw path collection with 3 offsets
                         closing axes
                         closing figure
                         """)


def test_text():
    fig, ax = plt.subplots()
    ax.set_xlabel("my x label")
    ax.set_ylabel("my y label")
    ax.set_title("my title")
    ax.text(0.5, 0.5, "my text")

    _assert_output_equal(fake_renderer_output(fig, FakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw text 'my text' None
                         draw text 'my x label' xlabel
                         draw text 'my y label' ylabel
                         draw text 'my title' title
                         closing axes
                         closing figure
                         """)


def test_path():
    fig, ax = plt.subplots()
    ax.add_patch(plt.Circle((0, 0), 1))
    ax.add_patch(plt.Rectangle((0, 0), 1, 2))

    _assert_output_equal(fake_renderer_output(fig, FakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw path with 25 vertices
                         draw path with 4 vertices
                         closing axes
                         closing figure
                         """)


def test_Figure():
    """ if the fig is not associated with a canvas, FakeRenderer shall
    not fail. """
    fig = plt.Figure()
    ax = fig.add_subplot(111)
    ax.add_patch(plt.Circle((0, 0), 1))
    ax.add_patch(plt.Rectangle((0, 0), 1, 2))

    _assert_output_equal(fake_renderer_output(fig, FakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw path with 25 vertices
                         draw path with 4 vertices
                         closing axes
                         closing figure
                         """)


def test_multiaxes():
    fig, ax = plt.subplots(2)
    ax[0].plot(range(4))
    ax[1].plot(range(10))

    _assert_output_equal(fake_renderer_output(fig, FakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw path with 4 vertices
                         closing axes
                         opening axes
                         draw path with 10 vertices
                         closing axes
                         closing figure
                         """)


def test_image():
    np.random.seed(0)  # image size depends on the seed
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.imshow(np.random.random((10, 10)),
              cmap=plt.cm.jet, interpolation='nearest')
    _assert_output_equal(fake_renderer_output(fig, FakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw image of size 1240 
                         closing axes
                         closing figure
                         """)


def test_legend():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], label='label')
    ax.legend().set_visible(False)
    _assert_output_equal(fake_renderer_output(fig, FakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw path with 3 vertices
                         opening legend
                         closing legend
                         closing axes
                         closing figure
                         """)


@pytest.mark.xfail
def test_legend_dots():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], label='label')
    ax.plot([2, 2, 2], 'o', label='dots')
    ax.legend().set_visible(True)
    _assert_output_equal(fake_renderer_output(fig, FullFakeRenderer),
                         """
                         opening figure
                         opening axes
                         draw line with 3 points
                         draw 3 markers
                         opening legend
                         draw line with 2 points
                         draw text 'label' None
                         draw 2 markers
                         draw text 'dots' None
                         draw path with 5 vertices
                         closing legend
                         closing axes
                         closing figure
                         """)


def test_blended():
    fig, ax = plt.subplots()
    ax.axvline(0)
    assert_warns(UserWarning, fake_renderer_output, fig, FakeRenderer)


if __name__ == "__main__":
    print("hello test")
