[![CI with install](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/ci_with_install.yml/badge.svg?branch=main)](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/ci_with_install.yml)

[![Upload Python Package](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/python-publish.yml/badge.svg)](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/python-publish.yml)

A Python package for plotting the positions, directions or energy distributions of OpenMC sources.

# Installation

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

```python
import openmc
import openmc_source_plotter  # extends openmc.IndependentSource with plotting functions

# initialises a new source object
my_source = openmc.IndependentSource()

# sets the energy distribution to a muir distribution neutrons for DT fusion neutrons
my_source.energy = openmc.stats.muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# plots the particle energy distribution
plot = my_source.plot_source_energy(n_samples=2000)

plot.show()
```

![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/143615694-a3578115-f8a2-4971-bf26-458177b4f113.png)

## Plot of energy distribution of two sources

```python
import openmc
import openmc_source_plotter  # extends openmc.IndependentSource with plotting functions

# initialises a new source object
my_dt_source = openmc.IndependentSource()

# sets the energy distribution to a muir distribution DT neutrons
my_dt_source.energy = openmc.stats.muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# initialises a new source object
my_dd_source = openmc.IndependentSource()
# sets the energy distribution to a muir distribution DD neutrons
my_dd_source.energy = openmc.stats.muir(e0=2080000.0, m_rat=2.0, kt=20000.0)

# plots the particle energy distribution by building on the first plot
figure1 = my_dd_source.plot_source_energy(n_samples=10000)
figure2 = my_dt_source.plot_source_energy(figure=figure1, n_samples=10000)

figure2.show()
```

![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/151376414-fb1555eb-61d1-4c82-bc4d-a05f62819c5d.png)

## Plot direction of particles

```python
import openmc
import openmc_source_plotter  # extends openmc.IndependentSource with plotting functions

# initializes a new source object
my_source = openmc.IndependentSource()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# plots the particle energy distribution
plot = my_source.plot_source_direction(n_samples=200)

plot.show()
```

![openmc particle source direction plot](https://user-images.githubusercontent.com/8583900/143615706-3b3a8467-0233-42d6-a66c-d536c80a01d8.png)


<!-- ## Plot gamma spectrum of particles

```python
import openmc
import openmc_source_plotter  # adds plot_gamma_emission plot to materials


openmc.config["chain_file"] = "chain-endf.xml"

my_material = openmc.Material()
my_material.add_nuclide("Xe135", 1e-12)
my_material.add_nuclide("U235", 1)
my_material.add_nuclide("U238", 1)
my_material.add_nuclide("Co60", 1e-9)
my_material.volume = 1  # must be set so number of atoms can be found

# adds labels to the most active 3 gamma energies
plt = my_material.plot_gamma_emission(label_top=3)
plt.xscale("log")  # modify axis from default settings
plt.savefig("gamma_spec.png")
```

![openmc gamma spectrum](https://user-images.githubusercontent.com/8583900/228280129-b8160e18-9ca9-4b20-a4e1-d2948908daf6.png) -->

## Plot position of particles

```python
import openmc
import openmc_source_plotter  # extends openmc.IndependentSource with plotting functions

# initialises a new source object
my_source = openmc.IndependentSource()

# the distribution of radius is just a single value
radius = openmc.stats.Discrete([10], [1])

# the distribution of source z values is just a single value
z_values = openmc.stats.Discrete([0], [1])

# the distribution of source azimuthal angles
# values is a uniform distribution between 0 and 2 Pi
angle = openmc.stats.Uniform(a=0.0, b=2 * 3.14159265359)

# this makes the ring source using the three distributions and a radius
my_source.space = openmc.stats.CylindricalIndependent(
    r=radius, phi=angle, z=z_values, origin=(0.0, 0.0, 0.0)
)

# plots the particle energy distribution
plot = my_source.plot_source_position()

plot.show()
```


![openmc particle source position plot](https://user-images.githubusercontent.com/8583900/179424915-bee56a87-6214-46ef-8625-92b8f4cbd1b3.png)


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
