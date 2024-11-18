## API Key Required

- Create your app token from https://data.cityofchicago.org/

- Create a file and name it `.env` at project base path

- Place the app token inside `.env` and name it as `API_KEY = "your_token"`

**Note:** Make sure to add `.env` to `.gitignore`

## Installation

To install conda environment in current path, do:

```conda env create -p env -f environment.yml```

To update environment.yml, do:

```conda env export --no-builds -p env > environment.yml```

Remove conda environment, do:

`conda remove -p env --all`