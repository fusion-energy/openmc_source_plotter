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
def test_model():
    # initialises a new source object
    my_source = openmc.IndependentSource()

    # sets the location of the source to x=0 y=0 z=0
    my_source.space = openmc.stats.Point((1.0, 2.0, 3.0))

    # sets the direction to isotropic
    my_source.angle = openmc.stats.Isotropic()

    # sets the energy distribution to 100% 14MeV neutrons
    my_source.energy = openmc.stats.Discrete([15e6], [1])

    my_source.particle = "photon"

    settings = openmc.Settings()
    settings.particles = 1
    settings.batches = 1
    settings.source = my_source

    materials = openmc.Materials()

    sph = openmc.Sphere(r=9999999999, boundary_type="vacuum")
    cell = openmc.Cell(region=-sph)
    geometry = openmc.Geometry([cell])

    model = openmc.Model(geometry, materials, settings)

    return model


def test_sample_initial_particles(test_model):
    particles = sample_initial_particles(this=test_model, n_samples=43)
    for particle in particles:
        assert particle.E == 15e6
        assert str(particle.particle) == "photon"
        assert particle.r == (1.0, 2.0, 3.0)
    assert len(particles) == 43


def test_energy_plot_with_bins(test_model):
    plot = plot_source_energy(
        this=test_model,
        n_samples=10,
        energy_bins=np.linspace(0, 20e6, 100),
    )
    assert isinstance(plot, go.Figure)


def test_energy_plot(test_model):
    plot = plot_source_energy(this=test_model, n_samples=10)
    assert isinstance(plot, go.Figure)
    assert len(plot.data[0]["x"]) == 1


def test_position_plot(test_model):
    plot = plot_source_position(this=test_model, n_samples=10)
    assert isinstance(plot, go.Figure)


def test_direction_plot(test_model):
    plot = plot_source_direction(this=test_model, n_samples=10)
    assert isinstance(plot, go.Figure)


def test_energy_plot_with_figure(test_model):
    base_figure = go.Figure()
    plot = plot_source_energy(this=test_model, figure=base_figure, n_samples=10)
    assert isinstance(plot, go.Figure)
    assert len(plot.data[0]["x"]) == 1


def test_position_plot_with_figure(test_model):
    base_figure = go.Figure()
    plot = plot_source_position(this=test_model, figure=base_figure, n_samples=10)
    assert isinstance(plot, go.Figure)


def test_direction_plot_with_figure(test_model):
    base_figure = go.Figure()
    plot = plot_source_direction(this=test_model, figure=base_figure, n_samples=10)
    assert isinstance(plot, go.Figure)
