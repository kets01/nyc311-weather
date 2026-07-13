import json

ns = "https://github.com/kets01/nyc311-weather#"

def e(label, etype, extra=None):
    d = {"prov:label": label, "prov:type": etype}
    if extra:
        d.update(extra)
    return d

entities = {
    "ex:src_nyc311_portal": e("NYC Open Data portal, dataset erm2-nwe9", "prov:Entity",
                               {"prov:location": "https://data.cityofnewyork.us/d/erm2-nwe9"}),
    "ex:src_noaa_portal": e("NOAA NCEI portal, station USW00094728", "prov:Entity",
                             {"prov:location": "https://www.ncei.noaa.gov/access/services/data/v1"}),
    "ex:raw_311_jan_feb": e("data/raw/311_2025-01_2025-02_downloaded_2026-07-12.csv", "prov:Entity",
                             {"prov:generatedAtTime": "2026-07-12T00:00:00"}),
    "ex:raw_311_jul_aug": e("data/raw/311_2025-07_2025-08_downloaded_2026-07-12.csv", "prov:Entity",
                             {"prov:generatedAtTime": "2026-07-12T00:00:00"}),
    "ex:raw_weather": e("data/raw/weather_centralpark_2025_downloaded_2026-07-12.csv", "prov:Entity",
                         {"prov:generatedAtTime": "2026-07-12T00:00:00"}),
    "ex:profiling_report_311": e("docs/311_profiling_report.html", "prov:Entity",
                                  {"prov:generatedAtTime": "2026-07-13T00:00:00"}),
    "ex:clean_311": e("data/processed/311_clean.csv", "prov:Entity",
                       {"prov:generatedAtTime": "2026-07-13T00:00:00"}),
    "ex:clean_weather": e("data/processed/weather_clean.csv", "prov:Entity",
                           {"prov:generatedAtTime": "2026-07-13T00:00:00"}),
    "ex:joined_analysis_daily": e("data/processed/analysis_daily.csv", "prov:Entity",
                                   {"prov:generatedAtTime": "2026-07-13T00:00:00"}),
}

fig_sources = {
    "fig_00": ("figures/fig_00_weather_overview.png", "act_explore_weather", ["ex:raw_weather"]),
    "fig_01": ("figures/fig_01_requests_vs_tmax.png", "act_analyze", ["ex:joined_analysis_daily"]),
    "fig_02": ("figures/fig_02_heat_vs_tmin.png", "act_analyze", ["ex:joined_analysis_daily"]),
    "fig_03": ("figures/fig_03_flooding_vs_prcp.png", "act_analyze", ["ex:joined_analysis_daily"]),
    "fig_04": ("figures/fig_04_correlation_heatmap.png", "act_analyze", ["ex:joined_analysis_daily"]),
    "fig_05": ("figures/fig_05_missingno_matrix.png", "act_assess_quality", ["ex:raw_311_jan_feb", "ex:raw_311_jul_aug"]),
    "fig_06": ("figures/fig_06_case_duration_hist.png", "act_assess_quality", ["ex:raw_311_jan_feb", "ex:raw_311_jul_aug"]),
    "fig_07": ("figures/fig_07_provenance_chain.png", "act_build_diagram", []),
}
for key, (label, _, _) in fig_sources.items():
    entities[f"ex:{key}"] = e(label, "prov:Entity", {"prov:generatedAtTime": "2026-07-13T00:00:00"})

activities = {
    "ex:act_download": {"prov:label": "notebooks/00_download.ipynb", "prov:type": "prov:Activity"},
    "ex:act_explore_311": {"prov:label": "notebooks/01_explore_311.ipynb", "prov:type": "prov:Activity"},
    "ex:act_explore_weather": {"prov:label": "notebooks/02_explore_weather.ipynb", "prov:type": "prov:Activity"},
    "ex:act_assess_quality": {"prov:label": "notebooks/03_quality.ipynb", "prov:type": "prov:Activity"},
    "ex:act_integrate": {"prov:label": "notebooks/04_integrate.ipynb", "prov:type": "prov:Activity"},
    "ex:act_analyze": {"prov:label": "notebooks/05_analysis.ipynb", "prov:type": "prov:Activity"},
    "ex:act_build_diagram": {"prov:label": "notebooks/build_fig07_provenance_diagram.py", "prov:type": "prov:Activity"},
}

agent = {"ex:kemki": {"prov:label": "kemki", "prov:type": "prov:Person"}}

was_generated_by = {}
i = 1
for k in ["ex:raw_311_jan_feb", "ex:raw_311_jul_aug", "ex:raw_weather"]:
    was_generated_by[f"_:wgb{i}"] = {"prov:entity": k, "prov:activity": "ex:act_download"}
    i += 1
was_generated_by[f"_:wgb{i}"] = {"prov:entity": "ex:profiling_report_311", "prov:activity": "ex:act_explore_311"}
i += 1
for k in ["ex:clean_311", "ex:clean_weather", "ex:joined_analysis_daily"]:
    was_generated_by[f"_:wgb{i}"] = {"prov:entity": k, "prov:activity": "ex:act_integrate"}
    i += 1
for key, (_, act, _) in fig_sources.items():
    was_generated_by[f"_:wgb{i}"] = {"prov:entity": f"ex:{key}", "prov:activity": f"ex:{act}"}
    i += 1

used = {}
i = 1
for src in ["ex:src_nyc311_portal", "ex:src_noaa_portal"]:
    used[f"_:u{i}"] = {"prov:activity": "ex:act_download", "prov:entity": src}
    i += 1
for k in ["ex:raw_311_jan_feb", "ex:raw_311_jul_aug"]:
    used[f"_:u{i}"] = {"prov:activity": "ex:act_explore_311", "prov:entity": k}
    i += 1
used[f"_:u{i}"] = {"prov:activity": "ex:act_explore_weather", "prov:entity": "ex:raw_weather"}
i += 1
for k in ["ex:raw_311_jan_feb", "ex:raw_311_jul_aug", "ex:raw_weather"]:
    used[f"_:u{i}"] = {"prov:activity": "ex:act_assess_quality", "prov:entity": k}
    i += 1
    used[f"_:u{i}"] = {"prov:activity": "ex:act_integrate", "prov:entity": k}
    i += 1
used[f"_:u{i}"] = {"prov:activity": "ex:act_analyze", "prov:entity": "ex:joined_analysis_daily"}
i += 1

was_derived_from = {}
i = 1
for k in ["ex:raw_311_jan_feb", "ex:raw_311_jul_aug"]:
    was_derived_from[f"_:wdf{i}"] = {"prov:generatedEntity": k, "prov:usedEntity": "ex:src_nyc311_portal"}
    i += 1
was_derived_from[f"_:wdf{i}"] = {"prov:generatedEntity": "ex:raw_weather", "prov:usedEntity": "ex:src_noaa_portal"}
i += 1
for k in ["ex:raw_311_jan_feb", "ex:raw_311_jul_aug"]:
    was_derived_from[f"_:wdf{i}"] = {"prov:generatedEntity": "ex:clean_311", "prov:usedEntity": k}
    i += 1
was_derived_from[f"_:wdf{i}"] = {"prov:generatedEntity": "ex:clean_weather", "prov:usedEntity": "ex:raw_weather"}
i += 1
for k in ["ex:clean_311", "ex:clean_weather"]:
    was_derived_from[f"_:wdf{i}"] = {"prov:generatedEntity": "ex:joined_analysis_daily", "prov:usedEntity": k}
    i += 1
for key, (_, _, sources) in fig_sources.items():
    for src in sources:
        was_derived_from[f"_:wdf{i}"] = {"prov:generatedEntity": f"ex:{key}", "prov:usedEntity": src}
        i += 1

was_associated_with = {
    f"_:waw{idx+1}": {"prov:activity": act, "prov:agent": "ex:kemki"}
    for idx, act in enumerate(activities.keys())
}

was_attributed_to = {
    f"_:wat{idx+1}": {"prov:entity": ent, "prov:agent": "ex:kemki"}
    for idx, ent in enumerate(
        ["ex:profiling_report_311", "ex:clean_311", "ex:clean_weather", "ex:joined_analysis_daily"]
        + [f"ex:{k}" for k in fig_sources]
    )
}

doc = {
    "$comment": "W3C PROV-JSON (https://www.w3.org/submissions/prov-json/) serialization of this project's pipeline. Human-readable equivalent: docs/FAIR_and_provenance.md.",
    "prefix": {
        "ex": ns,
        "prov": "http://www.w3.org/ns/prov#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
    },
    "entity": entities,
    "activity": activities,
    "agent": agent,
    "wasGeneratedBy": was_generated_by,
    "used": used,
    "wasDerivedFrom": was_derived_from,
    "wasAssociatedWith": was_associated_with,
    "wasAttributedTo": was_attributed_to,
}

with open("../docs/provenance.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2)
print("wrote docs/provenance.json")
