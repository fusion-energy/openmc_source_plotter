import openmc
from openmc_source_plotter import plot_gamma_emission

# you will need to install optional dependancies for this example
# pip install openmc_source_plotter[gammas]

# this path will need changing to point to your chain file
# openmc.config["chain_file"] = "chain-endf.xml"

my_material = openmc.Material()
my_material.add_nuclide("Xe135", 1e-12)
my_material.add_nuclide("U235", 1)
my_material.add_nuclide("U238", 1)
my_material.add_nuclide("Co60", 1e-9)
my_material.volume = 1  # must be set so number of atoms can be found

# adds labels to the most active 3 gamma energies
plt = plot_gamma_emission(material=my_material, label_top=3)
plt.xscale("log")  # modify axis from default settings
plt.savefig("gamma_spec.png")
