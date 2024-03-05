from openmc_plasma_source import tokamak_source
from openmc_source_plotter import plot_source_position
import openmc

my_sources = tokamak_source(
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
    ion_temperature_beta=6,
    angles=(0, 3.14),  # makes a sector of 0 radians to 3.14 radians
    sample_size=100,  # reduces the number of samples from a default of 1000 to reduce plot time
)

settings = openmc.Settings()
settings.Source = my_sources


# plots the particle energy distribution
plot = plot_source_position(settings)

plot.show()
