# Import SMAC-utilities
from smac.scenario.scenario import Scenario
from smac.facade.smac_facade import SMAC
from smac.tae.execute_func import ExecuteTAFuncDict
from sklearn import datasets

#import sklearn stuff
from sklearn.metrics import silhouette_score as silhouette_score
from sklearn.metrics import calinski_harabaz_score as c_h_score
import numpy as np
import pandas as pd

from sklearn.decomposition import  IncrementalPCA
from sklearn.preprocessing import OneHotEncoder as enc
from sklearn.impute import SimpleImputer as imp

import plotly.graph_objs as go
import dash_core_components as dcc
import dash_table

class AutoCA:

    def __init__(self, datapath: str, algo):
        if datapath == "test":
            self.dataset = pd.DataFrame(datasets.load_iris().data)
        else:
            self.dataset = pd.read_csv(datapath)

        self.algos = ["KMeans", "AffinityPropagation", "DBSCAN", "Birch", "AgglomerativeClustering", "MeanShift", "SpectralClustering"]

        #more tuner can be inserted here: preprocessing, only fast, special range of clusters?

        if algo == "all":
            pass
        else:
            self.algos = [i for i in self.algos if i in algo]

        print("setting up for algo(s) %s" %self.algos)

    def preprocess(self):

        self.dataset = imp(strategy="most_frequent").fit_transform(self.dataset)


    def optimise(self, maxtime = 200):

        self.tracker = {}

        for algo in self.algos:

            print("current algo is %s" %algo)
            self.current_algo = algo

            # build configure space
            from configure_algos import configure_algos
            cs = configure_algos(self.current_algo).configure_cs()

            # build scenario
            scenario = Scenario({"run_obj": "quality",
                                 "runcount_limit": 50,
                                 "cs": cs,
                                 "deterministic": "FALSE",
                                 "wallclock_limit": maxtime
                                 })

            # create ta
            ta = ExecuteTAFuncDict(self.eval_target)

            # optimise
            print("Optimising...")
           # print("starting at error rate of %.2f" % self.eval_target(cfg = {"cs": cs}))
            smac = SMAC(scenario=scenario,
                        tae_runner=ta)

            incumbent = smac.optimize()

            inc_value = self.eval_target(incumbent)

            if inc_value == 5:
                print("something did not work out with this algo. It might be the params or the algo does not know what to do with the data")
            else:
                print("optimized Value of %s is at %.2f" % (self.current_algo, inc_value))

            # save to tracker for end results
            self.tracker[self.current_algo] = {"metadata" : {"measure": inc_value,
                                                          "config": incumbent.configuration_space},
                                              "dataset" : {"dataset": self.dataset,
                                                           "labels": self.current_labels}}

    def eval_target(self, cfg):

        # get rid of non values which methods might not be able to process
        cfg = {k: cfg[k] for k in cfg if cfg[k]}

        # fit method with this dataset and extract labels to calc score
        from configure_algos import configure_algos
        self.current_labels = configure_algos(self.current_algo).prepare_algo(dataset = self.dataset, cfg = cfg)
        try:
            silhouette = silhouette_score(X=self.dataset, labels=self.current_labels)
        except:
            print("silhouette could not be assigned. N_clusters = 1. Proceeding")
            measure = 5
            return measure
        ch = c_h_score(X=self.dataset, labels=self.current_labels)
        #davies bouldin?

        # return combination of evaluation criteria
        measure = np.float(10 - (np.sqrt(np.sqrt(ch)) * (silhouette + 1)))
        return measure

    def create_plots(self):

        self.twoD_dataset = pd.DataFrame(IncrementalPCA(n_components=2, batch_size=10).fit_transform(self.dataset))
        self.threeD_dataset = pd.DataFrame(IncrementalPCA(n_components=3, batch_size=10).fit_transform(self.dataset))

        for algo in self.tracker:
            trace3D = go.Scatter3d(
                x=self.threeD_dataset[0],
                y=self.threeD_dataset[1],
                z=self.threeD_dataset[2],
                mode='markers',
                marker=dict(
                    size=12,
                    color=self.tracker[algo]["dataset"]["labels"],  # set color to an array/list of desired values
                    colorscale='Viridis',  # choose a colorscale
                    opacity=0.8
                )
            )
            data3D = [trace3D]
            layout3D = go.Layout(
                title="3D plot",
                margin=dict(
                    l=0,
                    r=0,
                    b=0,
                    t=0
                )
            )
            self.tracker[algo]["plot3D"] = go.Figure(data=data3D,
                                                     layout=layout3D)

            trace2D = go.Scatter(
                x=self.twoD_dataset[0],
                y=self.twoD_dataset[1],
                mode='markers',
                marker=dict(
                    size=12,
                    color=self.tracker[algo]["dataset"]["labels"],  # set color to an array/list of desired values
                    colorscale='Viridis',  # choose a colorscale
                    opacity=0.8
                )
            )
            data2D = [trace2D]
            layout2D = go.Layout(
                title="2D clustering anaylsis"
            )
            self.tracker[algo]["plot2D"] = go.Figure(data=data2D,
                                                     layout=layout2D)

        df = {"Algorithms": [algo for algo in self.tracker],
              "Performances": [self.tracker[algo]["metadata"]["measure"] for algo in self.tracker],
              "Configurations": [self.tracker[algo]["metadata"]["config"] for algo in self.tracker]}

        trace = go.Bar(
            x=df["Algorithms"],
            y=df["Performances"],
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5,
                )
            )
        )

        data = [trace]
        layout = go.Layout(
            title="Performance of different algorithms"
        )

        self.ranks = go.Figure(data=data,
                        layout=layout)