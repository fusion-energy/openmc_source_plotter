import openmc_source_plotter as osp
import openmc

# initializes a new source object
my_source = osp.SourceWithPlotting()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# plots the particle energy distribution
plot = my_source.plot_source_direction(n_samples=200)

plot.show()
