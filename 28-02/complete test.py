df = {"Algorithms": [algo for algo in self.tracker],
                "Performances": [self.tracker[algo]["metadata"]["measure"] for algo in self.tracker],
                "Configurations": [self.tracker[algo]["metadata"]["config"] for algo in self.tracker]}

        data = [go.Bar(
            x = df["Algorithms"],
            y = df["Performances"]
        )]
        layout = go.Layout(title = "Performance of Algorithms")

        self.rank = go.Figure(data = data, layout = layout)