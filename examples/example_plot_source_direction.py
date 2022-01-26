
import openmc_source_plotter as osp
import openmc

# initializes a new source object
my_source = openmc.Source()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# plots the particle energy distribution
plot = osp.plot_source_direction(
    source=my_source,
    number_of_particles=100,
    openmc_exec="/home/jshim/miniconda3/envs/openmc_0_11_0/bin/openmc",
)

plot.show()
