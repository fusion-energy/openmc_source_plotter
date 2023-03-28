#!/usr/bin/env python3

"""Provides functions for plotting source information"""

import typing

import numpy as np
import openmc
import openmc.lib
import plotly.graph_objects


def sample_initial_particles(self, n_samples: int = 1000, prn_seed: int = None):
    settings = openmc.Settings()
    settings.particles = 1
    settings.batches = 1
    settings.source = self
    settings.export_to_xml()

    materials = openmc.Materials()
    materials.export_to_xml()

    sph = openmc.Sphere(r=9999999999, boundary_type="vacuum")
    cell = openmc.Cell(region=-sph)
    geometry = openmc.Geometry([cell])

    geometry.export_to_xml()

    openmc.lib.init(output=False)
    particles = openmc.lib.sample_external_source(
        n_samples=n_samples, prn_seed=prn_seed
    )
    openmc.lib.finalize()

    return particles

def plot_source_energy(
    self,
    figure: plotly.graph_objects.Figure = None,
    n_samples: int = 2000,
    prn_seed: int = 1,
    energy_bins: typing.Union[str, np.array] = "auto",
    name: typing.Optional[str] = None,
):
    """makes a plot of the initial creation positions of an OpenMC source

    Args:
        figure: Optional base plotly figure to use for the plot. Passing in
            a pre made figure allows one to build up plots with from
            multiple sources. Defaults to None which makes a new figure for
            the plot.
        source: The openmc.Source object or list of openmc.Source objects
            to plot.
        n_samples: The number of source samples to obtain.
        prn_seed: The pseudorandom number seed
        energy_bins: Defaults to 'auto' which uses inbuilt auto binning in
            Numpy bins can also be manually set by passing in a numpy array
            of bin edges.
        name: the legend name to use
    """

    if figure is None:
        figure = plotly.graph_objects.Figure()
        figure.update_layout(
            title="Particle energy",
            xaxis={"title": "Energy (eV)"},
            yaxis={"title": "Probability"},
            showlegend=True,
        )

    data = self.sample_initial_particles(n_samples, prn_seed)

    e_values = [particle.E for particle in data]

    # Calculate pdf for source energies
    probability, bin_edges = np.histogram(e_values, bins=energy_bins, density=True)

    # scaling by strength
    probability = probability * self.strength

    # Plot source energy histogram
    figure.add_trace(
        plotly.graph_objects.Scatter(
            x=bin_edges[:-1],
            y=probability * np.diff(bin_edges),
            line={"shape": "hv"},
            hoverinfo="text",
            name=name,
        )
    )

    return figure

def plot_source_position(
    self,
    figure=None,
    n_samples: int = 2000,
    prn_seed: int = 1,
):
    """makes a plot of the initial creation positions of an OpenMC source(s)

    Args:
        figure: Optional base plotly figure to use for the plot. Passing in
            a pre made figure allows one to build up plots with from
            multiple sources. Defaults to None which makes a new figure for
            the plot.
        source: The openmc.Source object or list of openmc.Source objects
            to plot.
        n_samples: The number of source samples to obtain.
        prn_seed: The pseudorandom number seed
    """

    if figure is None:
        figure = plotly.graph_objects.Figure()
        figure.update_layout(
            title="Particle creation position",
            showlegend=True,
        )

    data = self.sample_initial_particles(n_samples, prn_seed)

    text = ["Energy = " + str(particle.E) + " eV" for particle in data]

    figure.add_trace(
        plotly.graph_objects.Scatter3d(
            x=[particle.r[0] for particle in data],
            y=[particle.r[1] for particle in data],
            z=[particle.r[2] for particle in data],
            hovertext=text,
            text=text,
            mode="markers",
            marker={
                "size": 2,
                "color": [particle.E for particle in data],
            },
        )
    )
    title = "Particle production coordinates coloured by energy"
    figure.update_layout(title=title)

    return figure

def plot_source_direction(
    self,
    figure=None,
    n_samples: int = 2000,
    prn_seed: int = 1,
):
    """makes a plot of the initial creation positions of an OpenMC source(s)

    Args:
        figure: Optional base plotly figure to use for the plot. Passing in
            a pre made figure allows one to build up plots with from
            multiple sources. Defaults to None which makes a new figure for
            the plot.
        source: The openmc.Source object or list of openmc.Source objects
            to plot.
        n_samples: The number of source samples to obtain.
        prn_seed: The pseudorandom number seed
    """

    figure = plotly.graph_objects.Figure()
    figure.update_layout(title="Particle initial directions")

    data = self.sample_initial_particles(n_samples, prn_seed)

    biggest_coord = max(
        max([particle.r[0] for particle in data]),
        max([particle.r[1] for particle in data]),
        max([particle.r[2] for particle in data]),
    )
    smallest_coord = min(
        min([particle.r[0] for particle in data]),
        min([particle.r[1] for particle in data]),
        min([particle.r[2] for particle in data]),
    )

    figure.add_trace(
        {
            "type": "scatter3d",
            "marker": {"color": "rgba(255,255,255,0)"},
            "x": [biggest_coord, smallest_coord],
            "y": [biggest_coord, smallest_coord],
            "z": [biggest_coord, smallest_coord],
        }
    )
    figure.add_trace(
        {
            "type": "cone",
            "cauto": False,
            "x": [particle.r[0] for particle in data],
            "y": [particle.r[1] for particle in data],
            "z": [particle.r[2] for particle in data],
            "u": [particle.u[0] for particle in data],
            "v": [particle.u[1] for particle in data],
            "w": [particle.u[2] for particle in data],
            "cmin": 0,
            "cmax": 1,
            "anchor": "tail",
            "colorscale": "Viridis",
            "hoverinfo": "u+v+w+norm",
            "sizemode": "absolute",
            "sizeref": 30,
            "showscale": False,
        }
    )

    return figure

"""
Extents the openmc.Source class to add source plotting
methods for energy, direction and position. Source sampling methods are
also provided for convenience. Additional methods are plot_source_energy(),
plot_source_position(), plot_source_direction(), sample_initial_particles()
"""
openmc.Source.sample_initial_particles = sample_initial_particles
openmc.Source.plot_source_energy = plot_source_energy
openmc.Source.plot_source_position = plot_source_position
openmc.Source.plot_source_direction = plot_source_direction
