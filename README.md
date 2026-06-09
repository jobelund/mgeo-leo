# MGEO · LEO Group — Seminars

Demos and materials from seminars of the **Lund University Earth Observation
(LEO) Group**, MGEO department. Each seminar is a self-contained project under
[`seminars/`](seminars/) — clone, `uv sync`, and run.

## Seminars

| Date | Topic | Folder |
|------|-------|--------|
| 2026-06-08 | Reactive Earth Observation with marimo + openEO (Sentinel-2) | [`seminars/2026-06-08-marimo-openeo/`](seminars/2026-06-08-marimo-openeo/) |

## Running a demo

```sh
git clone git@github.com:jobelund/mgeo-leo.git
cd mgeo-leo/seminars/<demo-folder>
uv sync
uv run marimo edit demo-openeo.py    # or: uv run marimo run demo-openeo.py
```

Each demo folder has its own `README.md` with full setup instructions (see the
[uv quick start](seminars/2026-06-08-marimo-openeo/README.md)).

## License

Released into the public domain under [**CC0 1.0 Universal**](LICENSE) — no
rights reserved.

---

Maintained by **José Beltrán** (jose.beltran@mgeo.lu.se) · LEO Group, MGEO
department, Lund University.
