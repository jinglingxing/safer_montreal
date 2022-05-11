
# Safe map for Montréal citizens
#### Project organization
- `README.md`: The top-level README for developers using this project.
- `data`: Public data from [Actes criminels](https://donnees.montreal.ca/ville-de-montreal/actes-criminels)
- `data_process`: Process data to have more features and create a map with `0.002*0.002` size of grids    
- `models`: Scripts to train models and then use trained models to make predictions 
- `notebooks`: Jupyter notebooks. Naming convention is a number (for ordering), the creator's initials, and a short - delimited description, e.g. 1.0-jqp-initial-data-exploration.
- `requirements.txt`: The requirements file for reproducing the analysis environment
- `visualization`: Scripts to create exploratory and results oriented visualizations

#### How to use venv

- create an env
```bash
virtualenv -p /usr/bin/python3 venv
```

- use the env
```bash
source venv/bin/activate
```

- install everything from env
```bash
pip3 install -r requirements.txt
```

- install a package
```
pip3 install ___
pip3 freeze > requirements.txt
```

