import openmc
import openmc.deplete
import openmc_source_plotter  # adds plot_gamma_emission plot to materials


openmc.config["chain_file"] = "chain-endf.xml"

my_material = openmc.Material()
my_material.add_nuclide("Xe135", 1e-12)
my_material.add_nuclide("U235", 1)
my_material.add_nuclide("U238", 1)
my_material.add_nuclide("Co60", 1e-9)
my_material.volume = 1

plt = my_material.plot_gamma_emission(label_top=3)
plt.xscale("log")  # modify axis from default settings
plt.savefig("gamma_spec.png")
