import openmc
import openmc_source_plotter  # overwrites the openmc.source method

# initializes a new source object
my_source = openmc.Source()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# plots the particle energy distribution
plot = my_source.plot_source_direction(n_samples=200)

plot.show()
