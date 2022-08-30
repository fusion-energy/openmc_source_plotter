from openmc_plasma_source import TokamakSource

# openmc_plasma_source makes use of this package and
# TokamakSource is a SourceWithPlotting object so it has
# access to the plotting methods

my_sources = TokamakSource(
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
).make_openmc_sources()


# plots the particle energy distribution
plot = None
for source in my_sources:
    plot = source.plot_source_position(figure=plot)

plot.show()
