import openmc_source_plotter as osp
import openmc
import numpy as np

# initialises a new source object
my_dt_source = openmc.Source()

# sets the energy distribution to a Muir distribution DT neutrons
my_dt_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# initialises a new source object
my_dd_source = openmc.Source()
# sets the energy distribution to a Muir distribution DD neutrons
my_dd_source.energy = openmc.stats.Muir(e0=2080000.0, m_rat=2.0, kt=20000.0)

# plots the particle energy distribution
plot = osp.plot_source_energy(source=[my_dt_source, my_dd_source], n_samples=10000)

plot.show()
