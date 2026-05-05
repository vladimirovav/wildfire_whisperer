# Wildfire-whisperer
Feasability study: A tool that allows to predict wildfires early using NDVI, SIF (Solar-Induced Fluorescence) from TROPOMI/S5P, weather data, boreal forest masks. 
---

## Project structure

```
/data        # A folder that holds the data_ should connect to the cloud
/docs        # Miscellaneous: Research papers, region maps, and project milestones.
/notebooks   # Individual exploratory analysis and prototyping.
/develop     # Folder that holds all the data, that will be stored here temporary before it gets pulles
/src         # Central repository for all projects scripts
/figures     # figures, visualizations, etc.
```

## Getting started

### 1. Prerequisites

You need [conda](https://docs.conda.io/en/latest/miniconda.html) installed on your machine. If you are unsure whether you have it, open a terminal and run:

```bash
conda --version
```

If you get a version number, you are good to go. If not, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (the lightweight version of conda).

### 2. Clone the repository

```bash
git clone https://github.com/vladimirovav/wildfire_whisperer.git
cd wildfire_whisperer
```

### 3. Create the environment

This reads `environment.yml` and installs all required packages into an isolated environment named `wildfire_whisperer`:

```bash
conda env create -f environment.yml
```

This will take several minutes on first run.

### 4. Activate the environment

You need to activate the environment each time you start a new terminal session before working on the project:

```bash
conda activate wildfire_whisperer
```

### 5. Update the environment

If the `environment.yml` file changes (e.g. a new package was added), update your local environment with:

```bash
conda env update -f environment.yml --prune
```

The `--prune` flag removes any packages that were removed from the file.

---

## Conventions

This project uses xarray for all gridded data. Do not load rasters into pandas DataFrames.

---

## Contributing

All new work goes into a feature branch and is merged into `develop` via a pull request. Nothing is pushed directly to `main` or `develop`.

```
main        # Stable snapshots only.
develop     # Integration branch. All feature branches merge here.
feature/*   # Your working branch. Branch off develop, PR back into develop.
```

1. Create a branch from `develop`:
   ```bash
   git checkout develop
   git checkout -b feature/your-feature-name
   ```

2. Switch between branches:
   ```bash
   git switch BRANCH_NAME
   ```
   
3. To keep your repository updated with changes others made run:
   ```bash
   git pull
   ```
   You should do this both for your feature and `develop` branches.
   
4. Commit your changes:
   ```bash
   git add .
   git commit -m "SHORT DESCRIPTION OF WHAT YOU DID"
   ```
   
5. Push changes:
   ```bash
   git push -u origin feature/your-feature-name
   ```
6. Open a pull request on GitHub from your branch into `develop`. A reviewer must approve it before it can be merged.
