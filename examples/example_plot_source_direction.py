import openmc
from openmc_source_plotter  import plot_source_direction

# initializes a new source object
my_source = openmc.IndependentSource()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# plots the particle energy distribution
plot = plot_source_direction(this=my_source, n_samples=200)

plot.show()
