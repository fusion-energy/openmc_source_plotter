import openmc
from openmc_source_plotter import plot_source_energy

# initialise a new source object
my_source = openmc.IndependentSource()

# sets the energy distribution to a muir distribution neutrons
my_source.energy = openmc.stats.muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# plots the particle energy distribution
plot = plot_source_energy(this=my_source, n_samples=10000)

plot.show()
