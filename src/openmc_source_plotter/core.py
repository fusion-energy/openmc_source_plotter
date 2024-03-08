#!/usr/bin/env python3

"""Provides functions for plotting source information"""

import typing
from tempfile import TemporaryDirectory
import numpy as np
import openmc
import openmc.lib
import plotly.graph_objects

import pkg_resources

system_openmc_version = pkg_resources.parse_version(openmc.__version__)
min_openmc_version = pkg_resources.parse_version("0.14.0")
if system_openmc_version < min_openmc_version:
    msg = (
        "openmc_source_plotter requires openmc version 0.14.0 or above. "
        f"You have openmc version {system_openmc_version} installed. "
        "Please update the version of openmc installed"
    )
    raise ImportError(msg)


def sample_initial_particles(this, n_samples: int = 1000, prn_seed: int = None):
    """smaples particles from the source.

    Args:
        this: The openmc source, settings or model containing the source to plot
        n_samples: The number of source samples to obtain.
        prn_seed: The pseudorandom number seed.
    """
    with TemporaryDirectory() as tmpdir:
        if isinstance(this, openmc.Model):
            model = this

        else:
            model = openmc.Model()

            materials = openmc.Materials()
            model.materials = materials

            sph = openmc.Sphere(r=99999999999, boundary_type="vacuum")
            cell = openmc.Cell(region=-sph)
            geometry = openmc.Geometry([cell])
            model.geometry = geometry

            if isinstance(this, openmc.Settings):
                model.settings = this

            else:  # source object
                settings = openmc.Settings()
                settings.particles = 1
                settings.batches = 1
                settings.source = this
                model.settings = settings

        model.export_to_model_xml()

        openmc.lib.init(output=False)
        particles = openmc.lib.sample_external_source(
            n_samples=n_samples, prn_seed=prn_seed
        )
        openmc.lib.finalize()

    return particles


def plot_source_energy(
    this,
    figure: plotly.graph_objects.Figure = None,
    n_samples: int = 2000,
    prn_seed: int = 1,
    energy_bins: typing.Union[str, np.array] = "auto",
    name: typing.Optional[str] = None,
    yaxis_type: str = "linear",
    xaxis_type: str = "linear",
    xaxis_units: str = "MeV",
):
    """makes a plot of the initial creation positions of an OpenMC source

    Args:
        this: The openmc source, settings or model containing the source to plot
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
        yaxis_type: The type (scale) to use for the Y axis. Options are 'log'
            or 'linear.
        xaxis_type: The type (scale) to use for the Y axis. Options are 'log'
            or 'linear.
        xaxis_units: The units to use for the x axis. Options are 'eV' or 'MeV'.
    """

    if xaxis_units not in ["eV", "MeV"]:
        raise ValueError(f"xaxis_units must be either 'eV' or 'MeV' not {xaxis_units}")

    if figure is None:
        figure = plotly.graph_objects.Figure()
        figure.update_layout(
            title="Particle energy",
            xaxis={"title": f"Energy [{xaxis_units}]", "type": xaxis_type},
            yaxis={"title": "Probability", "type": yaxis_type},
            showlegend=True,
        )

    data = sample_initial_particles(this, n_samples, prn_seed)

    e_values = [particle.E for particle in data]

    # Calculate pdf for source energies
    probability, bin_edges = np.histogram(e_values, bins=energy_bins, density=True)

    # scaling by strength
    if isinstance(this, openmc.SourceBase):
        probability = probability * this.strength
    energy = bin_edges[:-1]
    if xaxis_units == "MeV":
        energy = energy / 1e6
    # Plot source energy histogram
    figure.add_trace(
        plotly.graph_objects.Scatter(
            x=energy,
            y=probability * np.diff(bin_edges),
            line={"shape": "hv"},
            hoverinfo="text",
            name=name,
        )
    )

    return figure


def plot_source_position(
    this: typing.Union[openmc.SourceBase, openmc.Settings, openmc.Model],
    figure=None,
    n_samples: int = 2000,
    prn_seed: int = 1,
):
    """makes a plot of the initial creation positions of an OpenMC source(s)

    Args:
        this: The openmc source, settings or model containing the source to plot
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

    data = sample_initial_particles(this, n_samples, prn_seed)

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
    this: typing.Union[openmc.SourceBase, openmc.Settings, openmc.Model],
    figure=None,
    n_samples: int = 2000,
    prn_seed: int = 1,
):
    """makes a plot of the initial creation positions of an OpenMC source(s)

    Args:
        this: The openmc source, settings or model containing the source to plot
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

    data = sample_initial_particles(this, n_samples, prn_seed)

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
