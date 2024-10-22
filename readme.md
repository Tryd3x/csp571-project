To install conda environment in current path, do:

```conda env create -p env -f environment.yml```

To update environment.yml, do:

```conda env export --no-builds -p env > environment.yml```

Remove conda environment, do:

`conda remove -p env --all`
