import openmc_source_plotter as osp
import openmc
import numpy as np

# initialises a new source object
my_source = openmc.Source()

# sets the energy distribution to a Muir distribution neutrons
my_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# plots the particle energy distribution
plot = osp.plot_source_energy(
    source=my_source,
    number_of_particles=10000,
    energy_bins=np.linspace(0, 20e6, 100),
)

plot.show()
