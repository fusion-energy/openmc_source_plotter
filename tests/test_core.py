import openmc_source_plotter as osp
import openmc
import unittest
import numpy as np
import plotly.graph_objects as go


class TestUtils(unittest.TestCase):
    def setUp(self):

        # initialises a new source object
        my_source = openmc.Source()

        # sets the location of the source to x=0 y=0 z=0
        my_source.space = openmc.stats.Point((0, 0, 0))

        # sets the direction to isotropic
        my_source.angle = openmc.stats.Isotropic()

        # sets the energy distribution to 100% 14MeV neutrons
        my_source.energy = openmc.stats.Discrete([14e6], [1])

        self.my_source = my_source

        # makes an initial_source.h5 file with details of the particles
        self.initial_source_filename = osp.sample_initial_particles(
            source=my_source,
            n_samples=10,
        )

    def test_energy_plot(self):

        plot = osp.plot_source_energy(
            source=self.my_source,
            n_samples=10000,
            energy_bins=np.linspace(0, 20e6, 100),
        )
        assert isinstance(plot, go.Figure)

    def test_position_plot(self):

        plot = osp.plot_source_position(
            source=self.my_source,
        )
        assert isinstance(plot, go.Figure)

    def test_direction_plot(self):
        plot = osp.plot_source_direction(
            source=self.my_source,
            n_samples=100,
        )
        assert isinstance(plot, go.Figure)
