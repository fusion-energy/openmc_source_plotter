import openmc
from openmc_source_plotter import plot_source_energy

# initialises a new source object
my_dt_source = openmc.Source()

# sets the energy distribution to a muir distribution DT neutrons
my_dt_source.energy = openmc.stats.muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# initialises a new source object
my_dd_source = openmc.Source()
# sets the energy distribution to a muir distribution DD neutrons
my_dd_source.energy = openmc.stats.muir(e0=2080000.0, m_rat=2.0, kt=20000.0)

# plots the particle energy distribution
figure1 = plot_source_energy(this=my_dd_source, n_samples=10000)
figure2 = plot_source_energy(this=my_dt_source, figure=figure1, n_samples=10000)

figure2.show()
