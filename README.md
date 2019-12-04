# Examples (for users of the SeDuCe platform)

This projects aims at helping users of the [SeDuCe platform](https://seduce.fr) to get started with the data it exposes. It is composed of
several python scripts that illustrates what can be done with SeDuCe.

The scripts interract with the [SeDuCe API](https://api.seduce.fr/) which is documented here:
[https://api.seduce.fr/apidocs/](https://api.seduce.fr/apidocs/) 

## Installation

We assume user has a functionnal Python3 development environnment, configured with:
* Python 3.7 [(get it here!)](https://www.python.org/downloads/) 
* Pip library manager ([more info here](https://pip.pypa.io/en/stable/installing/))

First, clone this project using the following command:
```shell
git clone git@github.com:SeduceProject/examples.git
```

Then go at the root of the project, install the dependencies:
```shell
pip3 install -r requirements.txt
```

You should be able to run examples now!

## First example: displaying few data on ecotype-42

In this first example, several metrics is fetch from the server ecotype-42 (front temperature, back temperature and the power consumption from its two outlets). The script will display the minimum, the maximum and the average values for each of these metrics. The code is available in [examples/get_temp_and_power_data.py](examples/get_temp_and_power_data.py) of the cloned git repository.

Run the script with the following command:
```shell
python3 examples/get_temp_and_power_data.py
``` 

You should get the following result:
```shell
----  -------------------  ---------------  -----------------
      cumulated power (W)  front temp. (C)  back temp. (C)
mean  70.07274247491638    13.096088260497  30.72376611827479
min   0                    7.3              26.25
max   159                  18.31            33.5
----  -------------------  ---------------  -----------------
```

## Second example: displaying few data on ecotype-42

In this second example, several metrics is fetch from the server ecotype-42 (front temperature, back temperature and the power consumption from its two outlets). The script then plots all the metrics in a matplotlib figure. The code is available in [examples/draw_power_and_temp_ecotype_42.py](examples/draw_power_and_temp_ecotype_42.py) of the cloned git repository.

Run the script with the following command:
```shell
python3 examples/draw_power_and_temp_ecotype_42.py
``` 

It should produce a figure that looks like:
![figure_example_2](/assets/img/tutorial/figure_example2.png)