from setuptools import setup

setup(
    name = "AutoCA",
    version = "0.1",
    description = "A module for the automatic optimisation of clusteranalyses using SMAC and SK learn",
    author = "Felix Dörpmund",
    packages = "AutoCA",
    install_requires = [SMAC, scikit-learn, numpy, dash, dash_core_components, dash_html_components, dash_table, dash_renderer, plotly, dill]
)