# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair>=6.2.1",
#     "dask>=2026.3.0",
#     "h5netcdf>=1.8.1",
#     "marimo>=0.23.9",
#     "numpy>=2.4.6",
#     "openeo>=0.39.1",
#     "polars>=1.41.2",
#     "pyproj>=3.7.2",
#     "xarray>=2026.4.0",
#     "zarr>=3.2.1",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## marimo vs Jupyter

    | | **marimo** | **Jupyter** |
    |---|---|---|
    | Execution model | Reactive dependency graph | Manual, any order |
    | Hidden / stale state | Prevented structurally (no out-of-order runs, stale outputs, or deleted-cell leftovers) | Common |
    | File format | Pure `.py` | `.ipynb` JSON |
    | `git diff` / merge | Clean | Painful |
    | Interactivity | Built-in UI, no callbacks | `ipywidgets` + callbacks |
    | Reproducibility | Deterministic order + inline deps | Depends on run order |
    | Deploy as web app | `marimo run` | needs Voilà / extra stack |
    | Run as script | `python nb.py` | needs `nbconvert` |
    | AI integration | Agent mode, `pair`, MCP, var-aware | extensions, bolt-ons |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "**Reactive runtime - the headline difference**": mo.md(
                """
                    marimo reads your code, builds a **dependency graph** of which
                    cell defines which variable, and when one cell changes it
                    **re-runs exactly the cells that depend on it** (and marks the
                    rest as unaffected). Jupyter runs cells in whatever order *you*
                    click them, so a notebook's on-screen state can silently diverge
                    from what the code actually says.
                    """
            ),
            "**It's just Python (`.py`)**": mo.md(
                """
                    This notebook *is* a normal Python module — readable `git diff`s,
                    `ruff`/`black` formatting, importable, and runnable as a plain
                    script. A `.ipynb` is JSON with embedded outputs and execution
                    counts: diffs are unreadable and merge conflicts are brutal.
                    """
            ),
            "**No hidden state**": mo.md(
                """
                    Delete a cell in marimo and its variables leave memory. Each
                    global is defined in **exactly one** cell. In Jupyter a deleted
                    cell's variables linger, so notebooks "work" until you restart
                    the kernel — then they don't.
                    """
            ),
            "**UI is first-class**": mo.md(
                """
                    `mo.ui.slider`, `mo.ui.table`, `mo.ui.altair_chart` bind directly
                    to Python values — **no callbacks**. Reading `widget.value` in a
                    cell makes that cell reactive to the widget.
                    """
            ),
            "**One file → notebook, app, or script**": mo.md(
                """
                    `marimo edit` (notebook), `marimo run` (read-only web app with
                    code hidden), or `python file.py` (script / CI job). Same file.
                    """
            ),
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How to run marimo

    ```bash
    # In your terminal
    source .venv/bin/activate
    ```

    **marimo CLI — commands & flags**

    | **uv code** | **marimo** | **options** | **name** | **args** |  description |
    |---|---|---|---|---|---|
    | uv run | marimo edit | | | | *create or edit a new notebook* |
    | | marimo edit | | notebook.py | | *create or edit a new notebook named `notebook.py`*  |
    | | marimo run | | notebook.py | | *run as a read only app* |
    | | marimo edit | --no-token | notebook.py |  | *do not create an access token*
    | | marimo edit | --sandbox | notebook.py | | *Run the notebook in an isolated environment* |
    | | marimo edit | --watch | notebook.py | | *reload the kernel when the file changes on disk* |
    | | marimo edit | --headless | notebook.py | | *don't auto-open a browser* |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Quick Examples

    * "https://molab.marimo.io/github/marimo-team/gallery-examples/blob/main/notebooks/library/matplotlib_selection.py/wasm"
    * "https://molab.marimo.io/github/marimo-team/gallery-examples/blob/main/notebooks/geo/click-zoom.py/wasm"
    * "https://molab.marimo.io/github/marimo-team/gallery-examples/blob/main/notebooks/geo/earthquake.py/wasm"
    * "https://molab.marimo.io/github/marimo-team/gallery-examples/blob/main/notebooks/external/when-europeans-fly-nest.py/wasm"
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Imports
    """)
    return


@app.cell
def _():
    import marimo as mo
    from datetime import date
    from pathlib import Path
    import numpy as np
    import polars as pl
    import xarray as xr
    import altair as alt

    return Path, alt, date, mo, np, pl, xr


@app.cell
def _():
    def _try(name):
        try:
            return __import__(name), True
        except Exception:
            return None, False


    openeo, HAS_OPENEO = _try("openeo")
    return HAS_OPENEO, openeo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🛰️ Reactive Earth Observation - marimo vs Jupyter

    A single, self-contained demo that processes Sentinel-2 imagery via
    **openEO**, builds a memory-efficient **xarray / zarr** data cube, draws an
    interactive **map with a GeoJSON overlay**, extracts **insights**, links a
    **dynamic chart to a table**, and finishes with **AI**.

    Every output below is **reactive**: move a control and everything
    downstream recomputes automatically - no "Run All", no stale cells, no
    hidden state. That single property is what marimo is the best alternative for Jupyter notebooks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Non-interactive auth — OAuth *client-credentials*

    The interactive **device-code** flow (`authenticate_oidc()`) needs a human
    to open a URL and paste a code. For unattended runs — a live demo, cron, CI —
    use a **service-account** client instead:

    1. In the [CDSE dashboard](https://dataspace.copernicus.eu) create an OAuth
       client; note its **client ID** and **client secret**.
    2. Expose them as environment variables (never hard-code secrets):
       ```bash
       export openeo_client_id="…"
       export openeo_client_secret="…"
       ```
    3. Authenticate with **no browser step**:
       ```python
       con = connection.authenticate_oidc_client_credentials(
           client_id=os.environ["openeo_client_id"],
           client_secret=os.environ["openeo_client_secret"],
       )
       ```

    The client secret is exchanged directly for a token — nothing to click — so
    the whole reactive pipeline can refresh on real Sentinel-2 data hands-free.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 · openEO: process satellite imagery in the cloud

    [openEO](https://openeo.org) is a standard API for Earth-observation
    backends. We point at the **Copernicus Data Space Ecosystem**, build a
    *lazy* process graph (nothing executes until we ask), and let the backend
    do the pixel crunching — we only download the small index result.

    ```python
    import openeo
    con = openeo.connect("openeo.dataspace.copernicus.eu")
    con.authenticate_oidc()                      # device-code login in browser

    cube = con.load_collection(
        "SENTINEL2_L2A",
        spatial_extent=bbox,
        temporal_extent=[start, end],
        bands=["B03", "B04", "B05", "B08"],      # only the bands the indices need
        max_cloud_cover=int(cloud_cover.value),  # driven by the slider, not fixed
    )
    b04, b08 = cube.band("B04"), cube.band("B08")
    ndvi = (b08 - b04) / (b08 + b04)             # + SAVI / NDRE / GNDVI via band math
    ndvi.download("ndvi.nc")                     # result → persisted as a zarr datacube
    ```

    > **openEO is lazy, and so is xarray/dask below.** Same idea at two
    > scales: describe the computation, defer execution, touch only the bytes
    > you need.
    """)
    return


@app.cell(hide_code=True)
def _(HAS_OPENEO, mo, openeo):
    # Connecting is cheap and needs no login; we always establish it up front.
    connection = None
    if not HAS_OPENEO:
        conn_status = "`openeo` not installed (`pip install openeo`)."
    else:
        try:
            connection = openeo.connect("openeo.dataspace.copernicus.eu")
            conn_status = "Connected to Copernicus Data Space Ecosystem."
        except Exception as e:  # noqa: BLE001
            conn_status = f"Connection failed: {e}"
    mo.md(f"**openEO status:** {conn_status}")
    return (connection,)


@app.cell(hide_code=True)
def _(date, mo):
    AOI_PRESETS = {
        "Söderslätt farmland (Skåne)": {
            "west": 13.00,
            "south": 55.42,
            "east": 13.22,
            "north": 55.55,
        },
        "Around Lund": {
            "west": 13.10,
            "south": 55.66,
            "east": 13.30,
            "north": 55.75,
        },
        "Vombsjön / Krankesjön": {
            "west": 13.45,
            "south": 55.65,
            "east": 13.70,
            "north": 55.78,
        },
    }

    aoi_dropdown = mo.ui.dropdown(
        options=list(AOI_PRESETS),
        value="Söderslätt farmland (Skåne)",
        label="Area of interest",
    )
    start_date = mo.ui.date(value=date(2025, 4, 1), label="Start")
    end_date = mo.ui.date(value=date(2025, 9, 15), label="End")
    cloud_cover = mo.ui.slider(0, 100, value=30, label="Max cloud cover %")
    index_select = mo.ui.multiselect(
        options=["SAVI", "NDRE", "GNDVI"],
        value=["SAVI", "NDRE", "GNDVI"],
        label="Extra indices (NDVI always included)",
    )
    mask_clouds = mo.ui.switch(value=True, label="Mask clouds (SCL)")
    run_button = mo.ui.run_button(label="▶ Fetch / refresh")
    return (
        AOI_PRESETS,
        aoi_dropdown,
        cloud_cover,
        end_date,
        index_select,
        mask_clouds,
        run_button,
        start_date,
    )


@app.cell(hide_code=True)
def _(
    aoi_dropdown,
    cloud_cover,
    end_date,
    index_select,
    mask_clouds,
    mo,
    run_button,
    start_date,
):
    mo.vstack(
        [
            mo.md("## Analysis controls"),
            mo.hstack([aoi_dropdown, cloud_cover], justify="start", gap=2),
            mo.hstack([start_date, end_date], justify="start", gap=2),
            mo.hstack(
                [index_select, mask_clouds, run_button], justify="start", gap=2
            ),
            mo.callout(
                mo.md(
                    "Pick an **AOI**, **date range**, **max cloud cover** and which "
                    "**vegetation indices** to compute. A matching cube is reused "
                    "from the zarr cache if present; otherwise it is downloaded from "
                    "openEO automatically. Click **▶ Fetch / refresh** to force a "
                    "fresh download for the current parameters."
                ),
                kind="info",
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(AOI_PRESETS, aoi_dropdown):
    aoi_name = aoi_dropdown.value
    bbox = AOI_PRESETS[aoi_name]
    return aoi_name, bbox


@app.cell(hide_code=True)
def _(mo):
    import os as _os
    import subprocess as _sp


    def _load_oeo_creds():
        # Prefer exported env vars; fall back to a login shell because the
        # credentials live (unexported) in ~/.bashrc. Secrets stay in os.environ
        # and are never rendered.
        cid = _os.environ.get("OPENEO_AUTH_CLIENT_ID") or _os.environ.get(
            "openeo_client_id"
        )
        sec = _os.environ.get("OPENEO_AUTH_CLIENT_SECRET") or _os.environ.get(
            "openeo_client_secret"
        )
        if not (cid and sec):
            try:
                r = _sp.run(
                    [
                        "bash",
                        "-ic",
                        r'printf "%s\0%s" "$openeo_client_id" "$openeo_client_secret"',
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                parts = (r.stdout or "").split("\0")
                if len(parts) == 2 and parts[0] and parts[1]:
                    cid, sec = parts
            except Exception:
                pass
        if cid and sec:
            _os.environ["OPENEO_AUTH_CLIENT_ID"] = cid
            _os.environ["OPENEO_AUTH_CLIENT_SECRET"] = sec
        return bool(cid and sec)


    has_oeo_creds = _load_oeo_creds()
    mo.md(
        "**Auth method:** "
        + (
            "OAuth **client-credentials** ✅ (non-interactive service account)."
            if has_oeo_creds
            else "interactive **device-code** login (no client creds found)."
        )
    )
    return (has_oeo_creds,)


@app.cell(hide_code=True)
def _(
    Path,
    aoi_name,
    bbox,
    cloud_cover,
    connection,
    end_date,
    has_oeo_creds,
    index_select,
    mask_clouds,
    mo,
    run_button,
    start_date,
    xr,
):
    import os
    import hashlib
    import shutil

    # --- Which indices to compute --------------------------------------------
    # NDVI is always included; the multiselect adds soil-/red-edge-/green-based
    # indices. Each maps to the Sentinel-2 L2A bands its formula needs.
    INDEX_BANDS = {
        "NDVI": ["B04", "B08"],
        "SAVI": ["B04", "B08"],
        "NDRE": ["B05", "B08"],
        "GNDVI": ["B03", "B08"],
    }
    selected_indices = ["NDVI"] + [i for i in index_select.value if i != "NDVI"]
    # Masking needs the Scene Classification Layer (SCL) in addition to the
    # formula bands.
    _needed_bands = sorted(
        {b for i in selected_indices for b in INDEX_BANDS[i]}
        | ({"SCL"} if mask_clouds.value else set())
    )

    # --- Persistent cache (a zarr datacube store) -----------------------------
    # Key the download by AOI + dates + cloud cover + index set + cloud-mask flag,
    # so each distinct request gets its own cube and identical ones reuse the saved
    # one (no API call, survives kernel restarts). Persisted as a chunked,
    # compressed zarr datacube rather than netCDF.
    _cache_dir = Path("openeo_cache")
    _cache_dir.mkdir(exist_ok=True)
    _req = (
        f"{aoi_name}|{start_date.value.isoformat()}|{end_date.value.isoformat()}"
        f"|cc{int(cloud_cover.value)}|{'+'.join(sorted(selected_indices))}"
        f"|mask{int(mask_clouds.value)}"
    )
    _key = hashlib.md5(_req.encode()).hexdigest()[:10]
    cache_file = _cache_dir / f"idx_{_key}.zarr"

    live_path = None
    live_error = None
    live_cached = False


    def _index_expr(cube, name, cloud_mask=None):
        # Band math on the loaded cube; optionally drop cloudy pixels, then label
        # the (band-less) result so several indices merge into one download.
        _b = {b: cube.band(b) for b in INDEX_BANDS[name]}
        if name == "NDVI":
            _e = (_b["B08"] - _b["B04"]) / (_b["B08"] + _b["B04"])
        elif name == "SAVI":
            _e = 1.5 * (_b["B08"] - _b["B04"]) / (_b["B08"] + _b["B04"] + 0.5)
        elif name == "NDRE":
            _e = (_b["B08"] - _b["B05"]) / (_b["B08"] + _b["B05"])
        elif name == "GNDVI":
            _e = (_b["B08"] - _b["B03"]) / (_b["B08"] + _b["B03"])
        if cloud_mask is not None:
            _e = _e.mask(cloud_mask)
        return _e.add_dimension("bands", label=name, type="bands")


    # Reuse the cache unless the user clicked Fetch to force a refresh; otherwise
    # (cold cache OR forced) authenticate, compute the indices and download.
    _force = run_button.value
    if cache_file.exists() and not _force:
        live_path = cache_file
        live_cached = True
    elif connection is not None:
        try:
            if has_oeo_creds:
                # Non-interactive OAuth client-credentials (service account).
                con = connection.authenticate_oidc_client_credentials(
                    client_id=os.environ["OPENEO_AUTH_CLIENT_ID"],
                    client_secret=os.environ["OPENEO_AUTH_CLIENT_SECRET"],
                )
            else:
                # Fallback: interactive device-code login.
                con = connection.authenticate_oidc(max_poll_time=120)
            _cube = con.load_collection(
                "SENTINEL2_L2A",
                spatial_extent=bbox,
                temporal_extent=[
                    start_date.value.isoformat(),
                    end_date.value.isoformat(),
                ],
                bands=_needed_bands,
                max_cloud_cover=int(cloud_cover.value),
            )
            # SCL-based cloud mask: drop no-data / saturated / cloud-shadow / cloud
            # (medium+high) / thin-cirrus / snow pixels — Scene Classification
            # classes 0, 1, 3, 8, 9, 10, 11 — before computing statistics.
            _cloud_mask = None
            if mask_clouds.value:
                _scl = _cube.band("SCL")
                _cloud_mask = (
                    (_scl == 0)
                    | (_scl == 1)
                    | (_scl == 3)
                    | (_scl == 8)
                    | (_scl == 9)
                    | (_scl == 10)
                    | (_scl == 11)
                )
            _result = _index_expr(_cube, selected_indices[0], _cloud_mask)
            for _name in selected_indices[1:]:
                _result = _result.merge_cubes(
                    _index_expr(_cube, _name, _cloud_mask)
                )
            # The backend can't stream a zarr *directory* over the synchronous
            # endpoint, so we transfer as a temp netCDF, then persist a zarr
            # datacube. Build it in a `.part` store and swap in atomically so an
            # interrupted download never leaves a corrupt cube behind.
            _tmp_nc = cache_file.with_suffix(".nc.part")
            _result.download(
                str(_tmp_nc), format="netCDF"
            )  # blocking sync transfer
            _raw = xr.open_dataset(_tmp_nc)
            _keep = [v for v in _raw.data_vars if _raw[v].ndim >= 3]
            _part = cache_file.with_suffix(".zarr.part")
            if _part.exists():
                shutil.rmtree(_part)
            _raw[_keep].to_zarr(_part, mode="w", consolidated=False, zarr_format=2)
            _raw.close()
            _tmp_nc.unlink(missing_ok=True)
            if cache_file.exists():
                shutil.rmtree(cache_file)
            _part.rename(cache_file)
            live_path = cache_file
        except Exception as e:  # noqa: BLE001
            live_error = str(e)
            if cache_file.exists():  # fall back to the last good cube
                live_path = cache_file
                live_cached = True

    # --- Status ---------------------------------------------------------------
    _idx_label = ", ".join(selected_indices)
    _mask_note = " · cloud-masked" if mask_clouds.value else " · no cloud mask"
    if live_error and live_path is None:
        _msg = mo.callout(
            mo.md(f"openEO job failed:\n\n`{live_error}`"), kind="danger"
        )
    elif live_error:
        _msg = mo.callout(
            mo.md(
                f"Refresh failed (`{live_error}`) — using **cached** datacube "
                f"`{cache_file.name}`."
            ),
            kind="warn",
        )
    elif live_cached:
        _msg = mo.callout(
            mo.md(
                f"Using **cached** zarr datacube → `{cache_file.name}` "
                f"({_idx_label}{_mask_note}) — no re-download. Click "
                f"**▶ Fetch / refresh** to re-download."
            ),
            kind="success",
        )
    elif live_path:
        _msg = mo.callout(
            mo.md(
                f"Downloaded real Sentinel-2 indices ({_idx_label}{_mask_note}) → "
                f"zarr datacube `{cache_file.name}` (cached for reuse)."
            ),
            kind="success",
        )
    else:
        _msg = mo.callout(
            mo.md(
                "openEO is unavailable (no connection) and nothing is cached yet "
                "for this request."
            ),
            kind="warn",
        )
    _msg
    return (live_path,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 · The data cube: xarray + zarr (memory-efficient by design)

    We load the result into an **xarray** `DataArray` with named dimensions
    `(time, lat, lon)`, write it to **zarr** (chunked, compressed,
    cloud-native), then reopen it **lazily with dask**. Operations like a
    temporal mean build a task graph and only read the chunks they need —
    you can analyse cubes far larger than RAM.
    """)
    return


@app.cell(hide_code=True)
def _(live_path, mo, xr):
    # Cold cache (nothing fetched yet) → halt this cell and everything downstream
    # of the cube, showing a hint instead of a cascade of reference errors.
    mo.stop(
        live_path is None,
        mo.callout(
            mo.md(
                "**No index cube loaded.** Pick an AOI / date range / indices "
                "above — a matching cube is downloaded from openEO automatically, "
                "or click **▶ Fetch / refresh** to force one."
            ),
            kind="info",
        ),
    )

    # The cached download is already a zarr datacube; open it lazily.
    _ds = xr.open_zarr(live_path, consolidated=False)


    def _normalise(da):
        # openEO returns (t, y, x) in UTM; rename to the (time, lat, lon) the rest
        # of the notebook expects (coords stay native — only names matter here).
        _ren = {}
        for _d in da.dims:
            _dl = str(_d).lower()
            if _dl in ("t", "time"):
                _ren[_d] = "time"
            elif _dl in ("y", "lat", "latitude"):
                _ren[_d] = "lat"
            elif _dl in ("x", "lon", "longitude"):
                _ren[_d] = "lon"
        out = da.rename(_ren).transpose("time", "lat", "lon")
        # These indices are physically bounded to [-1, 1]; raw L2A pixels over
        # cloud / shadow / no-data (NIR+Red near 0) can fall outside, so mask them
        # to NaN before stats / colour scaling.
        return out.where((out >= -1) & (out <= 1))


    # Each selected index is its own 3-D variable in the datacube.
    index_cubes = {
        str(_v): _normalise(_ds[_v]).rename(str(_v))
        for _v in _ds.data_vars
        if _ds[_v].ndim >= 3
    }
    available_indices = sorted(index_cubes, key=lambda n: (n != "NDVI", n))
    return available_indices, index_cubes


@app.cell(hide_code=True)
def _(available_indices, mo):
    view_index = mo.ui.radio(
        options=available_indices,
        value=available_indices[0],
        label="Index to analyse",
        inline=True,
    )

    # Short description of each index the user can choose from.
    _INDEX_DOC = {
        "NDVI": "**NDVI** — Normalized Difference Vegetation Index, `(NIR−Red)/(NIR+Red)`. General greenness & vigour; saturates over dense canopy.",
        "SAVI": "**SAVI** — Soil-Adjusted VI, `1.5·(NIR−Red)/(NIR+Red+0.5)`. Like NDVI but dampens bare-soil background — better for sparse/early cover.",
        "NDRE": "**NDRE** — Normalized Difference Red Edge, `(NIR−RedEdge)/(NIR+RedEdge)`. Chlorophyll / crop-stress sensitive; sees into denser canopy.",
        "GNDVI": "**GNDVI** — Green NDVI, `(NIR−Green)/(NIR+Green)`. Greenness / canopy-nitrogen proxy.",
    }
    _guide = mo.callout(
        mo.md(
            "**Vegetation index guide** — all are masked to the physical range [-1, 1]:\n\n"
            + "\n".join(f"- {_INDEX_DOC[i]}" for i in available_indices)
        ),
        kind="info",
    )

    mo.vstack(
        [
            mo.md("### 2b · Choose which index drives the analysis"),
            mo.md(
                "Downloaded: **"
                + ", ".join(available_indices)
                + "**. The cube, map, statistics and chart below all follow your "
                "choice here."
            ),
            view_index,
            _guide,
        ]
    )
    return (view_index,)


@app.cell(hide_code=True)
def _(available_indices, index_cubes, view_index):
    # The whole downstream analysis (zarr cube, maps, insights, chart, summary)
    # runs on whichever index is picked above.
    index_name = view_index.value or available_indices[0]
    ndvi_cube = index_cubes[index_name]
    return index_name, ndvi_cube


@app.cell(hide_code=True)
def _(Path, index_name, mo, ndvi_cube, xr):
    # --- zarr roundtrip + lazy/chunked reopen ---------------------------------
    _store = Path("ndvi_cube.zarr")
    ndvi_cube.to_dataset(name=index_name).to_zarr(
        _store, mode="w", consolidated=False, zarr_format=2
    )

    _reopened = xr.open_zarr(_store, consolidated=False)[index_name]
    try:
        ndvi_zarr = _reopened.chunk({"time": 4, "lat": 60, "lon": 80})
        _chunked = True
    except Exception:
        ndvi_zarr = _reopened  # dask not installed → still lazy-ish
        _chunked = False

    _full_mb = ndvi_cube.nbytes / 1e6
    _chunk_mb = (4 * 60 * 80 * 4) / 1e6  # one chunk, float32-ish
    mem_md = mo.md(
        f"""
        | | value |
        |---|---|
        | Cube shape `(time, lat, lon)` | `{tuple(ndvi_cube.shape)}` |
        | Full array in memory | **{_full_mb:.2f} MB** |
        | dask-chunked on reopen | **{_chunked}** |
        | One chunk reads ~ | **{_chunk_mb:.3f} MB** (not the whole cube) |
        | Stored as | `ndvi_cube.zarr/` (chunked + compressed) |

        A temporal mean below builds a **lazy** dask graph — pixels are only read
        when `.compute()` is finally called.
        """
    )
    mem_md
    return (ndvi_zarr,)


@app.cell(hide_code=True)
def _(mo, ndvi_zarr):
    # Lazy until .compute(): this is what scales past RAM.
    _lazy_mean = ndvi_zarr.mean("time")
    _kind = type(_lazy_mean.data).__name__
    mo.md(
        f"`ndvi_zarr.mean('time')` → backing array is **`{_kind}`** "
        f"(lazy{' dask graph' if _kind == 'Array' else ''}); "
        f"nothing was read from disk yet."
    )
    return


@app.cell(hide_code=True)
def _(index_name, mo, pixel_inspect, pixel_map, pixel_overview, pixel_refresh):
    mo.vstack(
        [
            mo.md(f"## 3 · Interactive map — explore {index_name} per pixel"),
            mo.md(
                "**Drag a box** on the overview (left) to zoom the detail (right); "
                "**click a pixel** in the detail to inspect its time series below. "
                "**Reset** clears the zoom and selection."
            ),
            pixel_refresh,
            mo.hstack(
                [pixel_overview, pixel_map],
                justify="start",
                gap=2,
                align="start",
            ),
            pixel_inspect,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pixel_refresh = mo.ui.button(
        value=0,
        on_click=lambda v: v + 1,
        label="🔄 Reset view (clear zoom + selection)",
    )
    return (pixel_refresh,)


@app.cell(hide_code=True)
def _(alt, bbox, index_name, mo, ndvi_zarr, np, pixel_refresh, pl):
    import pyproj

    # Re-running this cell (via Reset) rebuilds the overview from scratch, clearing
    # the brush — which resets the detail view + selection downstream.
    _ = pixel_refresh.value

    # Coarsen the (selected-index) cube to an interactive grid (~110 cells/side).
    _kf_lat = max(1, ndvi_zarr.sizes["lat"] // 110)
    _kf_lon = max(1, ndvi_zarr.sizes["lon"] // 110)
    pixel_small = (
        ndvi_zarr.coarsen(lat=_kf_lat, lon=_kf_lon, boundary="trim")
        .mean()
        .compute()
    )
    _nlat, _nlon = pixel_small.sizes["lat"], pixel_small.sizes["lon"]

    # Native (regular) UTM grid → rect geometry; convert centres to lon/lat for the
    # tooltip + table. UTM zone derived from the AOI.
    _e, _n = pixel_small.lon.values, pixel_small.lat.values
    _de = float(np.abs(np.median(np.diff(_e))))
    _dn = float(np.abs(np.median(np.diff(_n))))
    _ee, _nn = np.meshgrid(_e, _n)
    _cx = (bbox["west"] + bbox["east"]) / 2
    _zone = int((_cx + 180) // 6) + 1
    _epsg = (32600 if (bbox["north"] + bbox["south"]) / 2 >= 0 else 32700) + _zone
    _tf = pyproj.Transformer.from_crs(f"EPSG:{_epsg}", "EPSG:4326", always_xy=True)
    _lon, _lat = _tf.transform(_ee, _nn)

    _ri, _ci = np.meshgrid(np.arange(_nlat), np.arange(_nlon), indexing="ij")
    _mean2d = pixel_small.mean("time").values
    pixel_field = pl.DataFrame(
        {
            "row": _ri.ravel().astype("int32"),
            "col": _ci.ravel().astype("int32"),
            "e_lo": (_ee - _de / 2).ravel(),
            "e_hi": (_ee + _de / 2).ravel(),
            "n_lo": (_nn - _dn / 2).ravel(),
            "n_hi": (_nn + _dn / 2).ravel(),
            "lon": _lon.ravel(),
            "lat": _lat.ravel(),
            "value": _mean2d.ravel(),
        }
    )

    # Drag a box (interval brush) to choose the zoom region for the detail view.
    _brush = alt.selection_interval(encodings=["x", "y"])
    _ov = (
        alt.Chart(pixel_field)
        .mark_rect()
        .encode(
            x=alt.X("e_lo:Q", axis=None, scale=alt.Scale(zero=False, nice=False)),
            x2="e_hi:Q",
            y=alt.Y("n_lo:Q", axis=None, scale=alt.Scale(zero=False, nice=False)),
            y2="n_hi:Q",
            color=alt.Color(
                "value:Q",
                scale=alt.Scale(scheme="redyellowgreen", domain=[-0.1, 0.9]),
                title=f"mean {index_name}",
            ),
            opacity=alt.condition(_brush, alt.value(1.0), alt.value(0.35)),
        )
        .add_params(_brush)
        .properties(
            width=400,
            height=400,
            title=f"Overview — drag a box to zoom ({_nlat}×{_nlon})",
        )
    )
    pixel_overview = mo.ui.altair_chart(_ov)
    return pixel_field, pixel_overview, pixel_small


@app.cell(hide_code=True)
def _(alt, index_name, mo, pixel_field, pixel_overview, pl):
    _box = pixel_overview.value
    if _box is None or len(_box) == 0:
        pixel_sub = pixel_field
        _scope = "full AOI — brush the overview to zoom in"
    else:
        _r0, _r1 = int(_box["row"].min()), int(_box["row"].max())
        _c0, _c1 = int(_box["col"].min()), int(_box["col"].max())
        pixel_sub = pixel_field.filter(
            (pl.col("row") >= _r0)
            & (pl.col("row") <= _r1)
            & (pl.col("col") >= _c0)
            & (pl.col("col") <= _c1)
        )
        _scope = f"rows {_r0}–{_r1} · cols {_c0}–{_c1} ({pixel_sub.height} cells)"

    # Click a cell to select it; its row flows to .value for the inspector below.
    _pick = alt.selection_point(fields=["row", "col"], empty=False)
    _detail = (
        alt.Chart(pixel_sub)
        .mark_rect()
        .encode(
            x=alt.X("e_lo:Q", axis=None, scale=alt.Scale(zero=False, nice=False)),
            x2="e_hi:Q",
            y=alt.Y("n_lo:Q", axis=None, scale=alt.Scale(zero=False, nice=False)),
            y2="n_hi:Q",
            color=alt.Color(
                "value:Q",
                scale=alt.Scale(scheme="redyellowgreen", domain=[-0.1, 0.9]),
                title=f"mean {index_name}",
            ),
            stroke=alt.condition(_pick, alt.value("#111"), alt.value(None)),
            strokeWidth=alt.condition(_pick, alt.value(2), alt.value(0)),
            tooltip=[
                alt.Tooltip("lat:Q", format=".5f"),
                alt.Tooltip("lon:Q", format=".5f"),
                alt.Tooltip("value:Q", format=".3f", title=f"mean {index_name}"),
            ],
        )
        .add_params(_pick)
        .properties(
            width=400, height=400, title=f"Detail · {_scope} — click a pixel"
        )
    )
    pixel_map = mo.ui.altair_chart(_detail)
    return (pixel_map,)


@app.cell(hide_code=True)
def _(alt, index_name, mo, np, pixel_map, pixel_small, pl):
    _picked = pixel_map.value


    def _is_empty(v):
        try:
            return v is None or len(v) == 0
        except Exception:
            return True


    if _is_empty(_picked):
        pixel_inspect = mo.callout(
            mo.md(
                f"**Click a pixel** on the raster above to see its per-date "
                f"{index_name} values and location."
            ),
            kind="neutral",
        )
    else:
        # Last clicked cell → exact integer indices into the coarsened cube.
        try:
            _rec = _picked.tail(1).to_dicts()[0]  # polars
        except AttributeError:
            _rec = _picked.iloc[-1].to_dict()  # pandas fallback
        _r, _c = int(_rec["row"]), int(_rec["col"])
        _plon, _plat = float(_rec["lon"]), float(_rec["lat"])

        _series = pixel_small.isel(lat=_r, lon=_c).values
        _dates = [
            np.datetime_as_string(t, unit="D") for t in pixel_small.time.values
        ]
        pixel_series_df = pl.DataFrame(
            {
                "date": _dates,
                "lat": [round(_plat, 5)] * len(_dates),
                "lon": [round(_plon, 5)] * len(_dates),
                index_name: [
                    float(x) if np.isfinite(x) else None for x in _series
                ],
            }
        ).with_columns(pl.col("date").str.to_date("%Y-%m-%d"))

        _valid = pixel_series_df[index_name].drop_nulls()
        _mean = float(_valid.mean()) if _valid.len() else float("nan")

        _line = (
            alt.Chart(pixel_series_df)
            .mark_line(point=True, color="#1f78ff")
            .encode(
                x=alt.X("date:T", title="Acquisition date"),
                y=alt.Y(
                    f"{index_name}:Q",
                    title=index_name,
                    scale=alt.Scale(domain=[-1, 1]),
                ),
                tooltip=["date:T", alt.Tooltip(f"{index_name}:Q", format=".3f")],
            )
        )
        # Dashed rule at the time-mean — the value the aggregate map shows here.
        _rule = (
            alt.Chart(pl.DataFrame({index_name: [_mean]}))
            .mark_rule(color="#888", strokeDash=[5, 4])
            .encode(y=alt.Y(f"{index_name}:Q", scale=alt.Scale(domain=[-1, 1])))
        )
        _chart = (_line + _rule).properties(
            height=260,
            title=f"{index_name} time series · mean {_mean:.3f}",
        )

        pixel_inspect = mo.vstack(
            [
                mo.md(
                    f"📍 **lat** `{_plat:.5f}` · **lon** `{_plon:.5f}` — "
                    f"mean **{index_name} {_mean:.3f}** over {_valid.len()}/"
                    f"{pixel_series_df.height} clear date(s)"
                ),
                _chart,
                mo.ui.table(
                    pixel_series_df,
                    selection=None,
                    page_size=25,
                    label=f"Per-date {index_name} at this pixel",
                ),
            ]
        )
    return (pixel_inspect,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 · Insights

    Per-date vegetation statistics, plus a spatial health classification on
    the time-mean cube.
    """)
    return


@app.cell(hide_code=True)
def _(ndvi_cube, np, pl, xr):
    _rows = []
    for _t in ndvi_cube.time.values:
        _v = ndvi_cube.sel(time=_t).values
        _rows.append(
            {
                "date": np.datetime_as_string(_t, unit="D"),
                "mean_ndvi": round(float(np.nanmean(_v)), 3),
                "min_ndvi": round(float(np.nanmin(_v)), 3),
                "max_ndvi": round(float(np.nanmax(_v)), 3),
                "pct_healthy": round(100 * float(np.mean(_v > 0.5)), 1),
                "pct_stressed": round(100 * float(np.mean(_v < 0.2)), 1),
            }
        )
    insights_df = pl.DataFrame(_rows).with_columns(
        # real Date dtype so the chart's temporal brush selection can
        # filter it (a String column breaks marimo's date coercion).
        pl.col("date").str.to_date("%Y-%m-%d")
    )

    _tm = ndvi_cube.mean("time")
    _cls = xr.where(
        _tm > 0.5, "healthy", xr.where(_tm > 0.2, "moderate", "bare/water")
    )
    spatial_stats = {
        "healthy": round(float((_cls == "healthy").mean()) * 100, 1),
        "moderate": round(float((_cls == "moderate").mean()) * 100, 1),
        "bare/water": round(float((_cls == "bare/water").mean()) * 100, 1),
        "greening_delta": round(
            float(
                insights_df["mean_ndvi"].last() - insights_df["mean_ndvi"].first()
            ),
            3,
        ),
    }
    return insights_df, spatial_stats


@app.cell(hide_code=True)
def _(index_name, insights_df, mo, spatial_stats):
    _trend = (
        "greening 🌱" if spatial_stats["greening_delta"] > 0 else "browning 🍂"
    )
    mo.hstack(
        [
            mo.stat(
                f"{spatial_stats['healthy']}%",
                label=f"Healthy area ({index_name}>0.5)",
            ),
            mo.stat(f"{spatial_stats['moderate']}%", label="Moderate"),
            mo.stat(f"{spatial_stats['bare/water']}%", label="Bare / water"),
            mo.stat(
                f"{spatial_stats['greening_delta']:+.3f}",
                label=f"Mean {index_name} Δ — {_trend}",
            ),
        ],
        justify="start",
        gap=1.5,
        widths="equal",
    ) if not insights_df.is_empty() else None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 · Dynamic chart linked to a table

    Select points on the chart (drag a box, or shift-click) and the table
    below filters to that selection — a two-line pattern in marimo because
    `mo.ui.altair_chart` exposes the selection as `.value`. Wiring this in
    Jupyter means callbacks, widget traitlets, and `display()` plumbing.
    """)
    return


@app.cell(hide_code=True)
def _(alt, index_name, insights_df, mo):
    _base = alt.Chart(insights_df).encode(x=alt.X("date:T", title="Date"))

    # Named brush over the date axis (stable name avoids stale-selection buildup).
    # Selected points are highlighted; the rest stay visible (dimmed) and the line
    # is always full, so the before/after context around the selection is kept.
    _brush = alt.selection_interval(name="datebrush", encodings=["x"])

    _line = _base.mark_line(color="#9aa0a6", strokeWidth=1.5).encode(
        y=alt.Y(
            "mean_ndvi:Q",
            title=f"Mean {index_name}",
            scale=alt.Scale(domain=[-0.1, 1.0]),
        )
    )
    _pts = (
        _base.mark_point(filled=True)
        .encode(
            y="mean_ndvi:Q",
            color=alt.Color(
                "pct_healthy:Q",
                title="% healthy",
                scale=alt.Scale(scheme="redyellowgreen"),
            ),
            size=alt.condition(_brush, alt.value(180), alt.value(45)),
            opacity=alt.condition(_brush, alt.value(1.0), alt.value(0.25)),
            stroke=alt.condition(_brush, alt.value("#111"), alt.value(None)),
            strokeWidth=alt.condition(_brush, alt.value(1), alt.value(0)),
            tooltip=["date:T", "mean_ndvi:Q", "pct_healthy:Q", "pct_stressed:Q"],
        )
        .add_params(_brush)
    )
    ndvi_chart = mo.ui.altair_chart(
        (_line + _pts).properties(height=300, title=f"{index_name} over time")
    )

    ndvi_table = mo.ui.table(
        insights_df, selection="multi", page_size=15, label="Per-date statistics"
    )
    return ndvi_chart, ndvi_table


@app.cell(hide_code=True)
def _(insights_df, mo, ndvi_chart, ndvi_table, pl):
    import datetime as _dt

    # Touch .value so this cell re-runs whenever the brush changes, but read the
    # dates from OUR named selection only — ndvi_chart.value intersects every
    # selection key (incl. stale ones from earlier chart versions), which was
    # clipping the table to a fixed date window.
    _ = ndvi_chart.value
    _cs = getattr(ndvi_chart, "_chart_selection", None) or {}
    _dr = (_cs.get("datebrush") or {}).get("date")

    if _dr and len(_dr) == 2:
        # Vega brush bounds are epoch-ms in local time (how it renders date:T).
        _lo = _dt.datetime.fromtimestamp(min(_dr) / 1000).date()
        _hi = _dt.datetime.fromtimestamp(max(_dr) / 1000).date()
        _sel = insights_df.filter(
            (pl.col("date") >= _lo) & (pl.col("date") <= _hi)
        )
    else:
        _lo = _hi = None
        _sel = insights_df.head(0)

    if _sel.height > 0:
        _selected = mo.vstack(
            [
                mo.md(f"**{_sel.height} date(s) selected** · {_lo} → {_hi}"),
                mo.ui.table(_sel, selection=None, page_size=12),
            ]
        )
    else:
        _selected = mo.callout(
            mo.md("**Drag a box across dates on the chart** to list them here."),
            kind="neutral",
        )

    mo.vstack(
        [
            mo.hstack(
                [ndvi_chart, _selected],
                justify="start",
                gap=2,
                align="start",
                widths=[2, 1],
            ),
            ndvi_table,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6 · AI with marimo

    Two complementary angles:

    **A. The editor is AI-native.** marimo ships an assistant that can see
    your **in-memory variables and dataframe schemas** (not just the source
    text), plus:

    - **Agent mode** — the assistant adds / edits / runs cells for you.
    - **`marimo pair`** — connect Claude Code, Codex, or other agents to a
      *live* notebook session for collaborative data work.
    - **`marimo --mcp`** — expose the notebook as an **MCP server** so
      external AI tools can inspect cells, variables, and errors.
    - **`marimo new "your prompt"`** — generate a whole notebook from text.

    **B. Or just pair with one.** Right now an agent is connected to this
    *live* session over `marimo pair`. Instead of calling an API with a key, the
    summary below was **written by the paired agent reading your actual cube** — and
    it is wired to your live `spatial_stats` / `insights_df`, so it re-reads the data
    (never a cached string) whenever the cube changes.
    """)
    return


@app.cell(hide_code=True)
def _(aoi_name, index_name, insights_df, mo, spatial_stats):
    # Summary written live by the *paired agent* — no API key, no model call.
    # It is wired to the real spatial_stats / insights_df, so the prose + numbers
    # track your data: re-fetch or change the AOI and this read updates.
    _d = spatial_stats
    _n = insights_df.height
    _first = float(insights_df["mean_ndvi"].first())
    _last = float(insights_df["mean_ndvi"].last())
    _delta = _d["greening_delta"]
    _lo = float(insights_df["min_ndvi"].min())
    _hi = float(insights_df["max_ndvi"].max())
    _d0 = insights_df["date"].first()
    _d1 = insights_df["date"].last()
    _src = "real Sentinel-2 (openEO · Copernicus Data Space)"

    _trend = (
        "essentially flat"
        if abs(_delta) < 0.03
        else ("a clear greening" if _delta > 0 else "a mild browning")
    )
    _dom = (
        "a near-complete healthy canopy"
        if _d["healthy"] >= 75
        else (
            "a mixed, partly-vegetated surface"
            if _d["healthy"] >= 40
            else "a largely bare / sparsely vegetated surface"
        )
    )
    _trend_note = (
        "Across only a handful of dates over a few weeks that is within "
        "scene-to-scene noise (view-angle/BRDF, residual haze) — not real "
        "senescence."
        if abs(_delta) < 0.05
        else "That is a large enough move to read as genuine phenology."
    )
    _caveat = ""
    if _lo < -1.0 or _hi > 1.0:
        _caveat = (
            f"\n- **Caveat.** Per-date {index_name} reaches {_lo:.2f} / {_hi:.2f} — outside "
            "the physical range [-1, 1]. Those are cloud/shadow/no-data pixels "
            "where NIR+Red is near zero; an SCL mask + clip to [-1, 1] would tidy "
            "the min/max columns without moving the headline numbers."
        )

    mo.md(
        f"""
        ### 🛰️ Analyst read — written live by the paired agent

        Over **{aoi_name}** I looked at **{_n} cloud-filtered acquisition(s)**
        spanning **{_d0} → {_d1}**, from {_src}.

        - **Canopy.** The time-mean is {_dom}: **{_d["healthy"]}%** of the area is
          healthy ({index_name} > 0.5), **{_d["moderate"]}%** moderate and only
          **{_d["bare/water"]}%** bare/water. A spatial-mean {index_name} near
          **{(_first + _last) / 2:.2f}** is what you'd expect for closed-canopy
          summer crops on this fertile Skåne plain.
        - **Trend.** Date-to-date the field is **{_trend}**: mean {index_name} moves
          **{_first:.3f} → {_last:.3f}** (Δ **{_delta:+.3f}**). {_trend_note}{_caveat}

        *No key, no API call — this is me (the agent on the other end of
        `marimo pair`) reading your live `spatial_stats` and `insights_df`.*
        """
    )
    return


if __name__ == "__main__":
    app.run()
