from numpy import isin
import openmc_source_plotter as osp
import openmc
import unittest
from pathlib import Path
import numpy as np
import plotly.graph_objects as go


class TestUtils(unittest.TestCase):
    def setUp(self):

        self.openmc_exec_dict = {
            "ci": "/opt/openmc/build/bin/openmc",
            "laptop": "/home/jshim/miniconda3/envs/openmc_0_11_0/bin/openmc",
            "desktop": "/home/jshimwell/miniconda3/envs/openmc_0_11_0/bin/openmc",
        }
        self.current_computer = "laptop"

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
        self.initial_source_filename = osp.create_initial_particles(
            source=my_source,
            number_of_particles=10,
            openmc_exec=self.openmc_exec_dict[self.current_computer],
        )

    def test_energy_plot(self):

        plot = osp.plot_source_energy(
            source=self.my_source,
            number_of_particles=10000,
            energy_bins=np.linspace(0, 20e6, 100),
        )
        assert isinstance(plot, go.Figure)

    def test_position_plot(self):

        plot = osp.plot_source_position(
            source=self.my_source,
            openmc_exec=self.openmc_exec_dict[self.current_computer],
        )
        assert isinstance(plot, go.Figure)

    def test_direction_plot(self):
        plot = osp.plot_source_direction(
            source=self.my_source,
            number_of_particles=100,
            openmc_exec=self.openmc_exec_dict["laptop"],
        )
        assert isinstance(plot, go.Figure)
