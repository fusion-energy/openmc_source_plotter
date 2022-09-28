import openmc
import matplotlib.pyplot as plt


class Material(openmc.Material):
    def plot_gamma_emission(
        self,
        threshold,
    ):

        import lineid_plot

        energies_to_label = []
        labels = []
        atoms = self.get_nuclide_atoms()
        for nuc, num_atoms in atoms.items():
            dists = []
            probs = []
            print(nuc)
            source_per_atom = openmc.data.decay_photon_energy(nuc)
            if source_per_atom is not None:
                dists.append(source_per_atom)
                probs.append(num_atoms)
                combo = openmc.data.combine_distributions(dists, probs)
                for p, x in zip(combo.p, combo.x):
                    if p > threshold:
                        print("   ", p, x)
                        energies_to_label.append(x)
                        labels.append(nuc)

        lineid_plot.plot_line_ids(
            self.decay_photon_energy.x,
            self.decay_photon_energy.p,
            energies_to_label,
            labels,
        )

        # plt.plot()
        plt.xlabel("Energy (eV)")
        # plt.xscale('log')
        plt.ylabel("Probability")
        return plt


openmc.Material = Material
