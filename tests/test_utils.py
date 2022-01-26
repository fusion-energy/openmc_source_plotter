import openmc_source_plotter as osp
import openmc
import unittest
from pathlib import Path


class TestUtils(unittest.TestCase):
    def setUp(self):

        self.openmc_exec_dict = {
            "ci": "/opt/openmc/build/bin/openmc",
            "laptop": "/home/jshim/miniconda3/envs/openmc_0_11_0/bin/openmc",
            "desktop": "/home/jshimwell/miniconda3/envs/openmc_0_11_0/bin/openmc",
        }

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
            openmc_exec=self.openmc_exec_dict["ci"],
        )

    def test_keys(self):

        key_values = [
            "x_values",
            "y_values",
            "z_values",
            "x_dir",
            "y_dir",
            "z_dir",
            "e_values",
        ]

        data = osp.get_particle_data(self.initial_source_filename)
        for key in key_values:
            assert key in data.keys()

    def test_initial_source_output_file(self):
        initial_source_filename = osp.create_initial_particles(
            source=self.my_source,
            number_of_particles=10,
            output_source_filename="new_initial_source.h5",
            openmc_exec=self.openmc_exec_dict["ci"],
        )

        assert initial_source_filename == "new_initial_source.h5"
        assert Path("new_initial_source.h5").exists()
        assert Path("initial_source.h5").exists() is False
