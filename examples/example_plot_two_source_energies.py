import openmc
import openmc_source_plotter  # overwrites the openmc.source method 

# initialises a new source object
my_dt_source = openmc.Source()

# sets the energy distribution to a Muir distribution DT neutrons
my_dt_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# initialises a new source object
my_dd_source = openmc.Source()
# sets the energy distribution to a Muir distribution DD neutrons
my_dd_source.energy = openmc.stats.Muir(e0=2080000.0, m_rat=2.0, kt=20000.0)

# plots the particle energy distribution
figure1 = my_dd_source.plot_source_energy(n_samples=10000)
figure2 = my_dt_source.plot_source_energy(figure=figure1, n_samples=10000)

figure2.show()
