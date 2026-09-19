"""Charge les ressources d'exemple de seed_resources.json dans l'API DevShelf.

Utilisation (l'API doit déjà tourner) :
    python3 seed.py
    python3 seed.py --api-url http://localhost:8000

Les ressources dont le titre existe déjà sont ignorées : le script peut donc
être relancé sans créer de doublons. N'utilise que la bibliothèque standard.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

SEED_FILE = Path(__file__).resolve().parent.parent / "seed_resources.json"


def request_json(url, payload=None):
    """GET si payload est None, sinon POST en JSON. Retourne la réponse décodée."""
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=10) as res:
        return json.load(res)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--api-url", default="http://localhost:8000")
    args = parser.parse_args()
    api = args.api_url.rstrip("/")

    seed = json.loads(SEED_FILE.read_text(encoding="utf-8"))

    try:
        existing_titles = {r["title"] for r in request_json(f"{api}/resources/")}
        created = skipped = 0
        for item in seed:
            if item["titre"] in existing_titles:
                skipped += 1
                print(f"  déjà présent : {item['titre']}")
                continue
            # Les champs du JSON sont en français, ceux de l'API en anglais.
            request_json(
                f"{api}/resources/",
                {
                    "title": item["titre"],
                    "category": item["categorie"],
                    "content": item["contenu"],
                },
            )
            created += 1
            print(f"  ajouté       : {item['titre']}")
    except (urllib.error.URLError, TimeoutError) as exc:
        sys.exit(
            f"Impossible de joindre l'API sur {api} ({exc}).\n"
            "Lance-la d'abord : uvicorn main:app --reload"
        )

    print(f"Terminé : {created} ajoutée(s), {skipped} ignorée(s).")


if __name__ == "__main__":
    main()
