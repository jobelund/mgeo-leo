# mgeo-leo — Reactive Earth Observation with marimo

A self-contained [marimo](https://marimo.io) notebook (`demo-openeo.py`) that
contrasts marimo's reactive runtime with Jupyter, built around a live
Earth-observation workflow: real **Sentinel-2** imagery via
[openEO](https://openeo.org) (NDVI + SAVI / NDRE / GNDVI with an SCL cloud
mask), a chunked **zarr** datacube, an interactive per-pixel map inspector,
and a dynamic chart linked to tables.

## Quick start

> Commands below are for macOS / Linux. Windows equivalents are noted inline.

### 1. Install the uv package manager

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternatives: `brew install uv`, `pipx install uv`, or `pip install uv`.
Verify the install:

```sh
uv --version
```

### 2. Initialize a uv project

```sh
uv init mgeo-leo
cd mgeo-leo
```

This scaffolds a `pyproject.toml`. To initialize **inside an existing folder**
(e.g. a clone of this repo), just run `uv init` in it. If you cloned this repo,
you can skip ahead — it already ships a `pyproject.toml` and `uv.lock`.

### 3. Create the virtual environment (Python 3.13.x)

```sh
uv venv --python 3.13
```

uv downloads a managed CPython 3.13 automatically if you don't have one. Pin a
specific patch with e.g. `uv venv --python 3.13.7`. The included
`.python-version` (`3.13`) is respected by uv on subsequent commands.

### 4. Source (activate) the environment

```sh
source .venv/bin/activate
```

- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- Windows (cmd): `.venv\Scripts\activate.bat`

(With uv you can also skip activation and prefix commands with `uv run`.)

### 5. Install marimo and its dependencies

```sh
uv add marimo openeo xarray zarr dask polars altair pyproj
```

If you cloned this repo (so `pyproject.toml` + `uv.lock` are present), install
the exact locked set instead:

```sh
uv sync
```

### 6. Run / edit the notebook — with and without sandbox

**Without sandbox** (uses the project virtual environment you just set up):

```sh
# Interactive editor. --no-token makes the server locally discoverable
uv run marimo edit demo-openeo.py --no-token

# Or serve it read-only as an app
uv run marimo run demo-openeo.py
```

**With sandbox** (an isolated, ephemeral environment built from the notebook's
inline [PEP 723](https://peps.python.org/pep-0723/) dependencies — your project
venv is left untouched):

```sh
uv run marimo edit --sandbox demo-openeo.py

# …or without adding marimo to the project at all, via uv's tool runner:
uvx marimo edit --sandbox demo-openeo.py
```

Useful extra flags: `--headless` (don't auto-open a browser) and `--watch`
(reload the kernel when the file changes on disk).

## openEO credentials (optional, for live data)

The notebook fetches real Sentinel-2 data from the
[Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu). For
unattended runs it uses an OAuth **client-credentials** service account — export
these before launching:

```sh
export openeo_client_id="…"
export openeo_client_secret="…"
```

Without them, the notebook falls back to the interactive device-code login the
first time you click **▶ Fetch from openEO**. Downloaded cubes are cached as
zarr datacubes under `openeo_cache/`, so repeated runs with the same parameters
need no network access.

## Credits

Maintained by **José Beltrán**. Created for a seminar (held **2026-06-08**)
within the **Lund University Earth Observation (LEO) Group** of the **MGEO
department**.
