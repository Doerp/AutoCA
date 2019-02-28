from smac.configspace import ConfigurationSpace
from ConfigSpace.hyperparameters import CategoricalHyperparameter, \
    UniformFloatHyperparameter, UniformIntegerHyperparameter
from ConfigSpace.conditions import InCondition
from sklearn import cluster as sk_clusters


class configure_algos:

    #insert tuner here. What kind of process should it be? big config space?

    def __init__(self, algo: str):
        self.algo = algo

    def configure_cs(self):

        cs = ConfigurationSpace()

        if self.algo == "KMeans":

            n_clusters = UniformIntegerHyperparameter("n_clusters", 2, 15, default_value = 3)
            init = CategoricalHyperparameter("init", ["random", "k-means++"], default_value = "k-means++")
            cs.add_hyperparameters([n_clusters, init])

        if self.algo == "AffinityPropagation":

            damping = UniformFloatHyperparameter("damping", 0.5, 1, default_value = 0.5)
            cs.add_hyperparameter(damping)

        if self.algo == "DBSCAN":

            eps = UniformFloatHyperparameter("eps", 0.5, 100, default_value = 2)
            min_samples = UniformIntegerHyperparameter("min_samples", 2, 150, default_value = 2)
            cs.add_hyperparameters([eps,min_samples])

        if self.algo == "Birch":

            threshold = UniformFloatHyperparameter("threshold", 0.1, 2, default_value = 0.5)
            branching_factor = UniformIntegerHyperparameter("branching_factor", 10, 100, default_value = 50)
            n_clusters = UniformIntegerHyperparameter("n_clusters", 2, 15, default_value = 3)
            cs.add_hyperparameters([threshold, branching_factor, n_clusters])

        if self.algo == "AgglomerativeClustering":

            n_clusters = UniformIntegerHyperparameter("n_clusters", 2, 15, default_value = 3)
            linkage = CategoricalHyperparameter("linkage", ["ward", "complete", "average", "single"], default_value = "ward")
            affinity = CategoricalHyperparameter("affinity", ["l1", "l2", "manhattan"], default_value = "manhattan")
            use_affinity = InCondition(child = affinity, parent = linkage, values = ["complete", "average", "single"])
            cs.add_hyperparameters([affinity, linkage, n_clusters])
            cs.add_condition(use_affinity)

        if self.algo == "MeanShift":

            bandwidth = UniformFloatHyperparameter("bandwidth", 0.5, 3, default_value = 1.5)
            cs.add_hyperparameter(bandwidth)

        if self.algo == "SpectralClustering":

            affinity = CategoricalHyperparameter("affinity", ["nearest_neighbors", "rbf"], default_value = "nearest_neighbors")
            n_neighbors = UniformIntegerHyperparameter("n_neighbors", 1, 10, default_value = 2)
            use_neighbors = InCondition(child = n_neighbors, parent = affinity, values = ["nearest_neighbors"])
            gamma = UniformFloatHyperparameter("gamma", 0.1, 3, default_value = 1)
            use_gamma = InCondition(child = gamma, parent = affinity, values = ["rbf"])
            n_clusters = UniformIntegerHyperparameter("n_clusters", 2,15, default_value = 3)
            cs.add_hyperparameters([affinity, n_neighbors, gamma, n_clusters])
            cs.add_conditions([use_neighbors, use_gamma])


        print("%s config space assigned!"%self.algo)
        return cs

    def prepare_algo(self, dataset, cfg):

        if self.algo == "KMeans":
            labels = sk_clusters.KMeans(**cfg).fit(dataset).labels_

        elif self.algo == "MeanShift":
            labels = sk_clusters.MeanShift(**cfg).fit(dataset).labels_

        elif self.algo == "DBSCAN":
            labels = sk_clusters.DBSCAN(**cfg).fit(dataset).labels_

        elif self.algo == "Birch":
            labels = sk_clusters.Birch(**cfg).fit(dataset).labels_

        elif self.algo == "AgglomerativeClustering":
            labels = sk_clusters.AgglomerativeClustering(**cfg).fit(dataset).labels_

        elif self.algo == "SpectralClustering":
            labels = sk_clusters.SpectralClustering(**cfg).fit(dataset).labels_

        elif self.algo == "AffinityPropagation":
            labels = sk_clusters.AffinityPropagation(**cfg).fit(dataset).labels_

        else:
            print("labels could not be assigned")

        return labels

