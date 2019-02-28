#generate report: upon choise of tuner
    #PCA and grafix comparing different cluster solutions?
    #tabs for different solutions of algorithms

    #KPIs of different clusters
    #why are they different and where lay the biggest differences

    #Metadata about the dataset



class report:

    def __init__(self, dataset, labels, config, algo):
        self.dataset = dataset
        self.labels = labels

        if type(config) == dict:
            self.type = "multiple"
        else:
            self.type = "normal"

        self.config = config
        self.algo = algo






