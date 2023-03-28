import openmc
import matplotlib.pyplot as plt


def plot_gamma_emission(
    self,
    label_top: int = None,
):
    """makes a plot of the gamma energy spectra for a material. The
    material should contain unstable nuclide which undergo gamma emission
    to produce a plot. Such materials can be made manually or obtained via
    openmc deplete simulations.

    Args:
        label_top: Optionally label the n highest activity energies with
            the nuclide that generates them.

    Returns:
        Matplotlib pyplot object.
    """

    plt.clf()
    if label_top:
        import lineid_plot

        energies_to_label = []
        labels = []
        possible_energies_to_label = []

        atoms = self.get_nuclide_atoms()
        for nuc, num_atoms in atoms.items():
            dists = []
            probs = []
            source_per_atom = openmc.data.decay_photon_energy(nuc)
            if source_per_atom is not None:
                dists.append(source_per_atom)
                probs.append(num_atoms)
                combo = openmc.data.combine_distributions(dists, probs)
                for p, x in zip(combo.p, combo.x):
                    possible_energies_to_label.append((nuc, p, x))

        possible_energies_to_label = sorted(
            possible_energies_to_label, key=lambda x: x[1], reverse=True
        )[:label_top]
        for entry in possible_energies_to_label:
            energies_to_label.append(entry[2])
            labels.append(entry[0])

        probs = []
        en = []
        energy_dis = self.decay_photon_energy
        for p in energy_dis.p:
            probs.append(0)
            probs.append(p)
            probs.append(0)
        for x in energy_dis.x:
            en.append(x)
            en.append(x)
            en.append(x)
        # print(en)
        # print(probs)
        lineid_plot.plot_line_ids(
            en,
            # self.decay_photon_energy.x,
            probs,
            # self.decay_photon_energy.p,
            energies_to_label,
            labels,
        )

    else:
        probs = []
        en = []
        energy_dis = self.decay_photon_energy
        for p in energy_dis.p:
            probs.append(0)
            probs.append(p)
            probs.append(0)
        for x in energy_dis.x:
            en.append(x)
            en.append(x)
            en.append(x)

        # plt.scatter(energy_dis.x, energy_dis.p)
        plt.plot(en, probs)
        # print(energy_dis.p)
        # print(energy_dis.x)
    plt.xlabel("Energy [eV]")
    plt.ylabel("Activity [Bq/s]")
    return plt


# patching the functionality into openmc
openmc.Material.plot_gamma_emission = plot_gamma_emission
