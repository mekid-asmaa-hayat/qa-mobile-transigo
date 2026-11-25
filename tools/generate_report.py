"""
Transforme un résultat JUnit (pytest) en rapport de campagne Markdown avec décision GO / NO-GO.

Usage : python tools/generate_report.py reports/campagne1-junit.xml docs/07-rapport-campagne-1.md "Campagne 1 — Sprint 12" "v1.4.0-rc1 (APP_DEFECTS=on)"
"""
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date

# Traçabilité cas de test -> anomalie (renseignée après qualification des échecs de la campagne 1)
ANOMALIES = {
    "CT-06": ("BUG-001", "Critique"), "CT-13": ("BUG-002", "Bloquant"), "CT-12": ("BUG-003", "Bloquant"),
    "CT-10": ("BUG-004", "Critique"), "CT-14": ("BUG-005", "Majeur"), "CT-18": ("BUG-006", "Majeur"),
    "CT-17": ("BUG-007", "Mineur"), "CT-16": ("BUG-008", "Mineur"),
}
US = {"CT-01": "US-01", "CT-02": "US-01", "CT-03": "US-02", "CT-04": "US-03", "CT-05": "US-03", "CT-06": "US-03",
      "CT-07": "US-03", "CT-08": "US-04/05", "CT-09": "US-04", "CT-10": "US-04", "CT-11": "US-04", "CT-12": "US-04",
      "CT-13": "US-05", "CT-14": "US-06", "CT-15": "US-06", "CT-16": "US-04", "CT-17": "Transverse", "CT-18": "US-02",
      "CT-19": "Transverse", "CT-20": "Transverse", "CT-21": "Transverse", "CT-22": "Transverse", "CT-23": "US-06"}
ICON = {"passed": "✅ OK", "failed": "❌ KO", "skipped": "⏭️ Non exécuté"}


def main(junit, out, title, version):
    root = ET.parse(junit).getroot()
    results = defaultdict(dict)
    labels = {}
    for tc in root.iter("testcase"):
        m = re.match(r"test_ct(\d+)_(\w+)\[(ios|android)\]", tc.get("name"))
        if not m:
            continue
        ct = f"CT-{int(m.group(1)):02d}"
        labels[ct] = m.group(2).replace("_", " ")
        status = "failed" if tc.find("failure") is not None or tc.find("error") is not None else \
                 "skipped" if tc.find("skipped") is not None else "passed"
        results[ct][m.group(3)] = status

    executions = sum(len(v) for v in results.values())
    ok_exec = sum(1 for v in results.values() for s in v.values() if s == "passed")
    ct_ok = [ct for ct, v in results.items() if all(s == "passed" for s in v.values())]
    ct_ko = sorted(ct for ct in results if ct not in ct_ok)
    open_bugs = [ANOMALIES[ct] for ct in ct_ko if ct in ANOMALIES]
    unknown = [ct for ct in ct_ko if ct not in ANOMALIES]
    by_sev = defaultdict(int)
    for _, sev in open_bugs:
        by_sev[sev] += 1
    blocking = by_sev["Bloquant"] + by_sev["Critique"] + by_sev["Majeur"] + len(unknown)
    decision = "🟢 **GO** — mise en production recommandée" if blocking == 0 else \
               "🔴 **NO-GO** — mise en production refusée en l'état"

    lines = [
        f"# Rapport de campagne — {title}", "",
        f"- **Version testée** : {version}",
        f"- **Date d'exécution** : {date.today().strftime('%d/%m/%Y')}",
        f"- **Environnement** : émulation d'appareils Playwright — profil iOS exécuté sur "
        f"{'WebKit (moteur Safari)' if os.environ.get('IOS_ENGINE', 'webkit') == 'webkit' else 'Chromium (WebKit indisponible sur le poste ; WebKit exécuté en CI)'}"
        f", profil Android sur Chromium",
        "- **Périmètre** : tests automatisés de recette (23 cas) × 2 profils d'appareils "
        "(iOS — iPhone 13 / Android — Pixel 7). Les 12 cas manuels sur device réel sont suivis dans le cahier de recette.",
        "", "## Synthèse", "",
        "| Indicateur | Valeur |", "|---|---|",
        f"| Cas de test automatisés | {len(results)} |",
        f"| Exécutions (cas × appareil) | {executions} |",
        f"| Exécutions OK | {ok_exec} / {executions} ({100 * ok_exec // max(executions, 1)} %) |",
        f"| Cas de test OK sur les 2 OS | {len(ct_ok)} / {len(results)} |",
        f"| Anomalies ouvertes | {len(open_bugs) + len(unknown)} "
        f"(Bloquant {by_sev['Bloquant']}, Critique {by_sev['Critique']}, Majeur {by_sev['Majeur']}, Mineur {by_sev['Mineur']}"
        f"{', non qualifiées ' + str(len(unknown)) if unknown else ''}) |",
        "", f"## Décision : {decision}", "",
        "Règle appliquée (cf. stratégie de recette §7) : **0 anomalie Bloquante, Critique ou Majeure ouverte** ; "
        "les Mineures sont acceptées si un contournement existe et qu'elles sont planifiées au sprint suivant.", "",
        "## Résultats détaillés", "",
        "| Cas | User Story | Intitulé | iOS | Android | Anomalie |", "|---|---|---|---|---|---|",
    ]
    for ct in sorted(results):
        bug = ""
        if ct in ct_ko and ct in ANOMALIES:
            b, sev = ANOMALIES[ct]
            bug = f"[{b}](anomalies/{b}.md) ({sev})"
        elif ct in ct_ko:
            bug = "À qualifier"
        lines.append(f"| {ct} | {US.get(ct, '')} | {labels[ct]} | {ICON[results[ct].get('ios', 'skipped')]} | "
                     f"{ICON[results[ct].get('android', 'skipped')]} | {bug} |")
    lines += ["", "_Rapport généré automatiquement par `tools/generate_report.py` à partir du fichier JUnit de la campagne._", ""]
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"{out} : {ok_exec}/{executions} OK — {'GO' if blocking == 0 else 'NO-GO'}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
