#!/usr/bin/env python3

"""Provides functions for plotting source information"""

import tempfile
from typing import List, Union

import numpy as np
import openmc
import openmc.lib
import plotly.graph_objects as go


def sample_initial_particles(
    source: openmc.source, n_samples: int = 1000, prn_seed: int = None
):

    settings = openmc.Settings()
    settings.particles = 1
    settings.batches = 1
    settings.source = source
    settings.export_to_xml()

    materials = openmc.Materials()
    materials.export_to_xml()

    sph = openmc.Sphere(r=9999999999, boundary_type="vacuum")
    cell = openmc.Cell(region=-sph)
    geometry = openmc.Geometry([cell])

    geometry.export_to_xml()

    openmc.lib.init()
    particles = openmc.lib.sample_external_source(
        n_samples=n_samples, prn_seed=prn_seed
    )
    openmc.lib.finalize()
    return particles


def plot_source_energy(
    source: Union[openmc.Source, List[openmc.Source]],
    n_samples: int = 2000,
    prn_seed: int = 1,
):
    """makes a plot of the initial creation postions of an OpenMC source(s)

    Args:
        source: The openmc.Source object or list of openmc.Source objects to plot.
        n_smaples: The number of source samples to obtain.
        prn_seed: The pseudorandom number seed
    """

    figure = go.Figure()

    if isinstance(source, openmc.Source):
        source = [source]

    for single_source in source:

        data = sample_initial_particles(single_source, n_samples, prn_seed)

        e_values = [particle.E for particle in data]

        # Calculate pdf for source energies
        probability, bin_edges = np.histogram(e_values, bins="auto", density=True)

        # Plot source energy histogram
        figure.add_trace(
            go.Scatter(
                x=bin_edges[:-1],
                y=probability * np.diff(bin_edges),
                line={"shape": "hv"},
                hoverinfo="text",
            )
        )

    figure.update_layout(
        title="Particle energy",
        xaxis={"title": "Energy (eV)"},
        yaxis={"title": "Probability"},
        showlegend=True,
    )

    return figure


def plot_source_position(
    source: Union[openmc.Source, List[openmc.Source]],
    n_samples: int = 2000,
    prn_seed: int = 1,
):
    """makes a plot of the initial creation postions of an OpenMC source(s)

    Args:
        source: The openmc.Source object or list of openmc.Source objects to plot.
        n_smaples: The number of source samples to obtain.
        prn_seed: The pseudorandom number seed
    """

    figure = go.Figure()

    if isinstance(source, openmc.Source):
        source = [source]

    for single_source in source:

        data = sample_initial_particles(single_source, n_samples, prn_seed)

        text = ["Energy = " + str(particle.E) + " eV" for particle in data]

        figure.add_trace(
            go.Scatter3d(
                x=[particle.r[0] for particle in data],
                y=[particle.r[1] for particle in data],
                z=[particle.r[2] for particle in data],
                hovertext=text,
                text=text,
                mode="markers",
                marker={
                    "size": 2,
                    # "color": data.E,
                },
            )
        )

    figure.update_layout(title="Particle production coordinates - coloured by energy")

    return figure


def plot_source_direction(
    source: Union[openmc.Source, List[openmc.Source]],
    n_samples: int = 2000,
    prn_seed: int = 1,
):
    """makes a plot of the initial creation postions of an OpenMC source(s)

    Args:
        source: The openmc.Source object or list of openmc.Source objects to plot.
        n_smaples: The number of source samples to obtain.
        prn_seed: The pseudorandom number seed
    """
    figure = go.Figure()

    if isinstance(source, openmc.Source):
        source = [source]

    for single_source in source:
        data = sample_initial_particles(single_source, n_samples, prn_seed)

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

    figure.update_layout(title="Particle initial directions")

    return figure
