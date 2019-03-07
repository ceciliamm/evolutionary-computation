# Problem Set 03

## Concepts:

* [Travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)
* [Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing)

## Files structure

* **`pset/`** is a Python module that contains
    * **`algorithms.py`** which have the SA implementation
    * **`models.py`** have the OOP abstraction of museums
    * **`data.py`** which exposes a `load_data()` function that reads a JSON file and translate it into the model's abstraction of museums and edges.
    * **`data.json`** contains the same information of `museos.sql` but
    structured as JSON.
* **`PSet Description.pdf`** is the original Problem Set definition.
* **`museos.sql`** is the initial dataset provided with the pset description
* **`Jupyter Notebooks`**:
    * **`PSet.ipynb`** contains some implementations of the problem
    like the cost function, candidate generation function and the multiple annealing schedule strategies. Also plot results.
