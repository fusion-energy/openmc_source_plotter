import openmc_source_plotter as osp
from openmc_plasma_source import TokamakSource
import openmc

my_source = TokamakSource(
    elongation=1.557,
    ion_density_centre=1.09e20,
    ion_density_peaking_factor=1,
    ion_density_pedestal=1.09e20,
    ion_density_separatrix=3e19,
    ion_temperature_centre=45.9,
    ion_temperature_peaking_factor=8.06,
    ion_temperature_pedestal=6.09,
    ion_temperature_separatrix=0.1,
    major_radius=9.06,
    minor_radius=2.92258,
    pedestal_radius=0.8 * 2.92258,
    mode="H",
    shafranov_factor=0.44789,
    triangularity=0.270,
    ion_temperature_beta=6
  ).make_openmc_sources()

# makes an initial_source.h5 file with details of the particles
initial_source_filename = osp.create_initial_particles(
    source=my_source,
    number_of_particles=10,
    openmc_exec="/home/jshim/miniconda3/envs/openmc_0_11_0/bin/openmc",
)

# plots the particle energy distribution
plot = osp.plot_position_from_initial_source(input_filename=initial_source_filename)

plot.show()
