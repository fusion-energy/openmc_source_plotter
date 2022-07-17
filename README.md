
A Python package for plotting the locations, directions or energy distributions of OpenMC sources.

# Installation

```bash
pip install openmc_source_plotter
```

# Features

The package provides functions to:

- extract the locations, directions and energy of particles
- visualise an ```openmc.Source``` with respect to:
    - direction
    - energy
    - location

# Example plots

## Plot of energy distribution of the source

```python
import openmc_source_plotter as osp
import openmc
import numpy as np

# initialises a new source object
my_source = openmc.Source()

# sets the energy distribution to a Muir distribution neutrons for DT fusion neutrons
my_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# plots the particle energy distribution
plot = osp.plot_source_energy(
    source=my_source,
    n_samples=2000,
)

plot.show()
```
![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/143615694-a3578115-f8a2-4971-bf26-458177b4f113.png)


## Plot of energy distribution of two sources

```python
import openmc_source_plotter as osp
import openmc
import numpy as np

# initialises a new source object
my_dt_source = openmc.Source()

# sets the energy distribution to a Muir distribution DT neutrons
my_dt_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# initialises a new source object
my_dd_source = openmc.Source()
# sets the energy distribution to a Muir distribution DD neutrons
my_dd_source.energy = openmc.stats.Muir(e0=2080000.0, m_rat=2.0, kt=20000.0)

# plots the particle energy distribution
plot = osp.plot_source_energy(
    source=[my_dt_source, my_dd_source],
    n_samples=10000,
)

plot.show()
```

![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/151376414-fb1555eb-61d1-4c82-bc4d-a05f62819c5d.png)

## Plot direction of particles

```python
import openmc_source_plotter as osp
import openmc

# initializes a new source object
my_source = openmc.Source()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# plots the particle energy distribution
plot = osp.plot_source_direction(
    source=my_source,
    n_samples=100,
)

plot.show()
```
![openmc particle source direction plot](https://user-images.githubusercontent.com/8583900/143615706-3b3a8467-0233-42d6-a66c-d536c80a01d8.png)


## Plot position of particles

```python

import openmc_source_plotter as osp
import openmc

# initialises a new source object
my_source = openmc.Source()

# the distribution of radius is just a single value
radius = openmc.stats.Discrete([10], [1])

# the distribution of source z values is just a single value
z_values = openmc.stats.Discrete([0], [1])

# the distribution of source azimuthal angles values is a uniform distribution between 0 and 2 Pi
angle = openmc.stats.Uniform(a=0.0, b=2 * 3.14159265359)

# this makes the ring source using the three distributions and a radius
my_source.space = openmc.stats.CylindricalIndependent(
    r=radius, phi=angle, z=z_values, origin=(0.0, 0.0, 0.0)
)

# plots the particle energy distribution
plot = osp.plot_source_position(source=my_source)

plot.show()

```

![openmc particle source position plot](https://user-images.githubusercontent.com/8583900/179424915-bee56a87-6214-46ef-8625-92b8f4cbd1b3.png)

# Usage

See the [examples folder](https://github.com/fusion-energy/openmc_source_plotter/tree/main/examples) for example usage scripts.
