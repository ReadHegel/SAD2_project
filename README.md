### Testing bayesian network inference on simulated boolean networks

How to run the programs:

after initialising conda, create two environments by navigating to the ``task1/conda_envs/`` directory using the files contained there by typing commands:
```
conda env create -f sad_generation.yml --name sad_generation
conda env create -f sad_inference.yml --name sad_inference
```
The ``sad_generation`` environment is used for generating the data and later stages of inference, the ``sad_inference`` is used for things dealing with the BNFinder library. Then you can use the scripts ``task1/generate_script.sh`` to generate data, and later ``task1/infer_script.sh`` to make inference about them. You do not need to activate conda environments before running the scripts, it is done automatically.
