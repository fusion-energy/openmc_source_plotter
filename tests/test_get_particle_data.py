import openmc_source_plotter as osp
import openmc
import unittest


class TestReactor(unittest.TestCase):
    def setUp(self):

        # initialises a new source object
        my_source = openmc.Source()

        # sets the location of the source to x=0 y=0 z=0
        my_source.space = openmc.stats.Point((0, 0, 0))

        # sets the direction to isotropic
        my_source.angle = openmc.stats.Isotropic()

        # sets the energy distribution to 100% 14MeV neutrons
        my_source.energy = openmc.stats.Discrete([14e6], [1])

        # makes an initial_source.h5 file with details of the particles
        self.initial_source_filename = osp.create_initial_particles(
            source=my_source,
            number_of_particles=10,
            openmc_exec="/opt/openmc/build/bin/openmc"
            # openmc_exec="/home/jshim/miniconda3/envs/openmc_0_11_0/bin/openmc",
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
