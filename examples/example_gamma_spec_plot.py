import openmc
import openmc.deplete
import openmc_source_plotter

openmc.config['chain_file']='chain-endf.xml'

my_material = openmc.Material()
my_material.add_nuclide('Xe135', 1e-12)
my_material.add_nuclide('U235', 1)
my_material.volume = 1
energy_dis= my_material.decay_photon_energy

plt = my_material.plot_gamma_emission(
        threshold=0.25e7,
)
plt.show()