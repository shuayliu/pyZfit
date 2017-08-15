# pyZfit
Electrochemical Impendance Spectrscopy Equivalent Circle fitting package

# Requirements:
- **[Python](http://www.python.org/) >= 3.x**
- **[Numpy](http://www.numpy.org/) >= latest**
- **[Pandas](http://pandas.pydata.org/) >= latest**
- [Matplotlib](http://matplotlib.org/) >= 2.x

# Data Format   
|Potential [1]| Frequency | Zreal | Zimag|
|--------------|-----------|-------|------|
|0.1 | 10000| 100| 100 | 100|   


[1]: POTENTION Position is defined at head of Zfit.py
# Usage: 
```
py Zfit.py
```

# Includes:
Config are defined in ```config.ini```

Models are defined in ```/Models``` . You can write your model as you like.

This Python script will exctact ECCs's parameter to ```./result/paras.txt ```and their statistic result to  ```./result/stat.txt```

# TODO:
- Probably will add some qtGUI in that

# Donate:    
Please turn to : [HERE](http://jonahliu.cf/donate)
