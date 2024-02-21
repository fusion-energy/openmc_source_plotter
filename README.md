[![CI with install](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/ci_with_install.yml/badge.svg?branch=main)](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/ci_with_install.yml)

[![Upload Python Package](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/python-publish.yml/badge.svg)](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/python-publish.yml)

A Python package for plotting the positions, directions or energy distributions of OpenMC sources.

# Installation

You will need to have OpenMC version 0.14.0 or newer installed first.

```bash
pip install openmc_source_plotter
```

# Features

The package simply extends the default ```openmc.IndependentSourceBase``` and ```openmc.Model``` to provides additional functions that:

- extract the positions, directions and energy of particles
- visualise a source with respect to:
  - direction
  - energy
  - position

Or just provide the initial particles with ```sample_initial_particles```

# Example plots

Below are some basic examples, for more examples see the [examples folder](https://github.com/fusion-energy/openmc_source_plotter/tree/main/examples) for example usage scripts.


## Plot of energy distribution of the source

:link:[Link](https://github.com/fusion-energy/openmc_source_plotter/blob/main/examples/example_plot_source_energy.py) to example script.

![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/143615694-a3578115-f8a2-4971-bf26-458177b4f113.png)

## Plot of energy distribution of two sources

:link:[Link](https://github.com/fusion-energy/openmc_source_plotter/blob/main/examples/example_plot_two_source_energies.py) to example script.

![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/151376414-fb1555eb-61d1-4c82-bc4d-a05f62819c5d.png)

## Plot direction of particles

:link:[Link](https://github.com/fusion-energy/openmc_source_plotter/blob/main/examples/example_plot_source_direction.py) to example script.

![openmc particle source direction plot](https://user-images.githubusercontent.com/8583900/143615706-3b3a8467-0233-42d6-a66c-d536c80a01d8.png)


## Plot position of particles

:link:[Link](https://github.com/fusion-energy/openmc_source_plotter/blob/main/examples/example_plot_source_position.py) to example script.


![openmc particle source position plot](https://user-images.githubusercontent.com/8583900/179424915-bee56a87-6214-46ef-8625-92b8f4cbd1b3.png)

## Plot labeled gamma lines from material

:link:[Link](https://github.com/fusion-energy/openmc_source_plotter/blob/main/examples/example_gamma_spec_plot.py) to example script.

![gamma spec with labels](examples/gamma_spec.png)


## Extract particle objects

A list of ```openmc.Particle``` objects can be obtained using ```model.sample_initial_particles()``` or ```openmc.SourceBase.sample_initial_particles()```

```python
import openmc
import openmc_source_plotter  # extents openmc.Model with sample_initial_particles method

settings = openmc.Settings()
settings.particles = 1
settings.batches = 1
my_source = openmc.IndependentSource()
my_source.energy = openmc.stats.muir(e0=14080000.0, m_rat=5.0, kt=20000.0)
settings.source = my_source
materials = openmc.Materials()
sph = openmc.Sphere(r=100, boundary_type="vacuum")
cell = openmc.Cell(region=-sph)
geometry = openmc.Geometry([cell])

model = openmc.Model(geometry, materials, settings)

particles = model.sample_initial_particles(n_samples=10)

print(particles)
>>>[<SourceParticle: neutron at E=1.440285e+07 eV>, <SourceParticle: neutron at E=1.397691e+07 eV>, <SourceParticle: neutron at E=1.393681e+07 eV>, <SourceParticle: neutron at E=1.470896e+07 eV>, <SourceParticle: neutron at E=1.460563e+07 eV>, <SourceParticle: neutron at E=1.420684e+07 eV>, <SourceParticle: neutron at E=1.413932e+07 eV>, <SourceParticle: neutron at E=1.412428e+07 eV>, <SourceParticle: neutron at E=1.464779e+07 eV>, <SourceParticle: neutron at E=1.391648e+07 eV>]

print(particles[0].E)
>>>1.440285e+07
```

## Related packages

Tokamak sources can also be plotted using the [openmc-plasma-source](https://github.com/fusion-energy/openmc-plasma-source) package

![openmc_source_plotter_openmc-plasma-source_tokamak](https://user-images.githubusercontent.com/8583900/187487894-ba0bd025-46f2-4c7d-8b15-3d260aed47a0.png)
