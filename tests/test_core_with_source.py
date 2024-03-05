import openmc
from openmc_source_plotter import (
    sample_initial_particles,
    plot_source_energy,
    plot_source_position,
    plot_source_direction,
)
import numpy as np
import plotly.graph_objects as go
import pytest


@pytest.fixture
def test_source():
    # initialises a new source object
    my_source = openmc.IndependentSource()

    # sets the location of the source to x=0 y=0 z=0
    my_source.space = openmc.stats.Point((4.0, 5.0, 6.0))

    # sets the direction to isotropic
    my_source.angle = openmc.stats.Isotropic()

    # sets the energy distribution to 100% 14MeV neutrons
    my_source.energy = openmc.stats.Discrete([14e6], [1])

    my_source.particle = "neutron"

    my_source = my_source
    return my_source


def test_sample_initial_particles(test_source):
    particles = sample_initial_particles(this=test_source, n_samples=42)
    for particle in particles:
        assert particle.E == 14e6
        assert str(particle.particle) == "neutron"
        assert particle.r == (4.0, 5.0, 6.0)
    assert len(particles) == 42


def test_energy_plot_with_bins(test_source):
    plot = plot_source_energy(
        this=test_source,
        n_samples=10,
        energy_bins=np.linspace(0, 20e6, 100),
    )
    assert isinstance(plot, go.Figure)


def test_energy_plot(test_source):
    plot = plot_source_energy(this=test_source, n_samples=10)
    assert isinstance(plot, go.Figure)
    assert len(plot.data[0]["x"]) == 1


def test_energy_plot_axis(test_source):
    plot = plot_source_energy(
        this=test_source,
        n_samples=10,
        xaxis_type="log",
        yaxis_type="linear",
        xaxis_units="eV",
    )
    plot = plot_source_energy(
        this=test_source,
        n_samples=10,
        xaxis_type="linear",
        yaxis_type="log",
        xaxis_units="MeV",
    )
    assert isinstance(plot, go.Figure)
    assert len(plot.data[0]["x"]) == 1


def test_position_plot(test_source):
    plot = plot_source_position(this=test_source, n_samples=10)
    assert isinstance(plot, go.Figure)


def test_direction_plot(test_source):
    plot = plot_source_direction(this=test_source, n_samples=10)
    assert isinstance(plot, go.Figure)


def test_energy_plot_with_figure(test_source):
    base_figure = go.Figure()
    plot = plot_source_energy(this=test_source, figure=base_figure, n_samples=10)
    assert isinstance(plot, go.Figure)
    assert len(plot.data[0]["x"]) == 1


def test_position_plot_with_figure(test_source):
    base_figure = go.Figure()
    plot = plot_source_position(this=test_source, figure=base_figure, n_samples=10)
    assert isinstance(plot, go.Figure)


def test_direction_plot_with_figure(test_source):
    base_figure = go.Figure()
    plot = plot_source_direction(this=test_source, figure=base_figure, n_samples=10)
    assert isinstance(plot, go.Figure)
