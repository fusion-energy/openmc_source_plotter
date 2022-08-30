[![CI with install](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/ci_with_install.yml/badge.svg)](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/ci_with_install.yml)

[![Python Flake8 Lint](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/lint.yaml/badge.svg)](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/lint.yaml)

[![Upload Python Package](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/python-publish.yml/badge.svg)](https://github.com/fusion-energy/openmc_source_plotter/actions/workflows/python-publish.yml)

A Python package for plotting the positions, directions or energy distributions of OpenMC sources.

# Installation

```bash
pip install openmc_source_plotter
```

# Features

The package simply extends the default ```openmc.Source``` to provides additional functions that:

- extract the positions, directions and energy of particles
- visualise an ```osp.SourceWithPlotting``` with respect to:
  - direction
  - energy
  - position

# Example plots

Below are some basic examples, for more examples see the [examples folder](https://github.com/fusion-energy/openmc_source_plotter/tree/main/examples) for example usage scripts.


## Plot of energy distribution of the source

```python
from openmc_source_plotter import SourceWithPlotting
import openmc
import numpy as np

# initialises a new source object
my_source = SourceWithPlotting()

# sets the energy distribution to a Muir distribution neutrons for DT fusion neutrons
my_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# plots the particle energy distribution
plot = my_source.plot_source_energy(n_samples=2000)

plot.show()
```

![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/143615694-a3578115-f8a2-4971-bf26-458177b4f113.png)

## Plot of energy distribution of two sources

```python
from openmc_source_plotter import SourceWithPlotting
import openmc
import numpy as np

# initialises a new source object
my_dt_source = SourceWithPlotting()

# sets the energy distribution to a Muir distribution DT neutrons
my_dt_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# initialises a new source object
my_dd_source = SourceWithPlotting()
# sets the energy distribution to a Muir distribution DD neutrons
my_dd_source.energy = openmc.stats.Muir(e0=2080000.0, m_rat=2.0, kt=20000.0)

# plots the particle energy distribution by building on the first plot
figure1 = my_dd_source.plot_source_energy(n_samples=10000)
figure2 = my_dt_source.plot_source_energy(figure=figure1, n_samples=10000)

figure2.show()
```

![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/151376414-fb1555eb-61d1-4c82-bc4d-a05f62819c5d.png)

## Plot direction of particles

```python
from openmc_source_plotter import SourceWithPlotting
import openmc

# initializes a new source object
my_source = SourceWithPlotting()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# plots the particle energy distribution
plot = my_source.plot_source_direction(n_samples=200)

plot.show()
```

![openmc particle source direction plot](https://user-images.githubusercontent.com/8583900/143615706-3b3a8467-0233-42d6-a66c-d536c80a01d8.png)

## Plot position of particles

```python
from openmc_source_plotter import SourceWithPlotting
import openmc

# initialises a new source object
my_source = SourceWithPlotting()

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

Tokamak sources can also be plotted using the [openmc-plasma-source](https://github.com/fusion-energy/openmc-plasma-source) package
![openmc_source_plotter_openmc-plasma-source_tokamak](https://user-images.githubusercontent.com/8583900/187487894-ba0bd025-46f2-4c7d-8b15-3d260aed47a0.png)
