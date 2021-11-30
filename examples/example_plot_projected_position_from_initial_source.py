import openmc_source_plotter as osp
import openmc
import numpy as np

# initialises a new source object
my_source = openmc.Source()

# the distribution of radius is just a single value
radius = openmc.stats.Discrete([10], [1])

# the distribution of source z values is just a single value
z_values = openmc.stats.Discrete([0], [1])

# the distribution of source azimuthal angles values is a uniform distribution between 0 and 2 Pi
angle = openmc.stats.Uniform(a=0.0, b=2 * 3.14159265359)

# this makes the ring source using the three distributions and a radius
my_source.space = openmc.stats.CylindricalIndependent(
    r=radius, phi=angle, z=z_values, origin=(0.0, 0.0, 0.0)
)


# makes an initial_source.h5 file with details of the particles
initial_source_filename = osp.create_initial_particles(
    source=my_source,
    number_of_particles=10,
    openmc_exec="/home/jshim/miniconda3/envs/openmc_0_11_0/bin/openmc",
)

# plots the particle energy distribution
plot = osp.plot_position_projected_from_initial_source(input_filename=initial_source_filename, axis='XY')

plot.show()
