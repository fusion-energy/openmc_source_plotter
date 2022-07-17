import openmc_source_plotter as osp
import openmc

# initializes a new source object
my_source = openmc.Source()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# plots the particle energy distribution
plot = osp.plot_source_direction(source=my_source, n_samples=200)

plot.show()
