import openmc_source_plotter as osp
import openmc
import numpy as np

# initializes a new source object
my_source = openmc.Source()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# makes an initial_source.h5 file with details of the particles
initial_source_filename = osp.create_initial_particles(
    source=my_source,
    number_of_particles=100,
    openmc_exec="/home/jshimwell/miniconda3/envs/openmc_0_11_0/bin/openmc",
)

# plots the particle energy distribution
plot = osp.plot_direction_from_initial_source(input_filename=initial_source_filename)

plot.show()
