import openmc
import openmc_source_plotter  # overwrites the openmc.source method

# initialises a new source object
my_source = openmc.Source()

# sets the location of the source to x=0 y=0 z=0
my_source.space = openmc.stats.Point((0, 0, 0))

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# sets the energy distribution to 100% 14MeV neutrons
my_source.energy = openmc.stats.Discrete([14e6], [1])

# gets the particle corrdiantes, energy and direction
data = my_source.sample_initial_particles()

print(data)
