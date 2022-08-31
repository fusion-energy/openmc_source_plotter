import openmc
import openmc_source_plotter  # overwrites the openmc.source method

# initialise a new source object
my_source = openmc.Source()

# sets the energy distribution to a Muir distribution neutrons
my_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# plots the particle energy distribution
plot = my_source.plot_source_energy(n_samples=10000)

plot.show()
