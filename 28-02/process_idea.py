exec(open("main.py").read())
exec(open("configure_algos.py").read())
import dill

test = AutoCA(datapath = "Wholesale_customers_data.csv", algo = "all")
test.preprocess()
test.optimise()
test.create_plots()

dill.dump(test, open("temp2", "wb"))

exec(open("app_testing.py").read())


