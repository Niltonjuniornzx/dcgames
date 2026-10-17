#!/usr/bin/env python3
"""Atualiza o catálogo sem apagar o último arquivo válido em caso de erro."""
import datetime
import json
import os
import pathlib
import tempfile
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "catalog.json"
URL = "https://discord.com/api/v10/applications/detectable"

def fetch():
    req = urllib.request.Request(URL, headers={
        "User-Agent": "DCGames-Catalog/1.0 (+https://github.com/Niltonjuniornzx/dcgames)",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=35) as resp:
        return json.load(resp)

def normalize(data):
    if isinstance(data, dict):
        data = data.get("applications") or data.get("data") or data.get("games")
    if not isinstance(data, list) or not data:
        raise ValueError("Fonte retornou catálogo vazio ou formato inesperado")
    games = []
    for item in data:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            continue
        exes = []
        seen = set()
        for entry in (item.get("executables") or []):
            if not isinstance(entry, dict):
                continue
            exe = entry.get("name") or entry.get("executable")
            if not isinstance(exe, str) or not exe.strip():
                continue
            platform = str(entry.get("os") or entry.get("platform") or "unknown").lower()
            key = (exe.casefold(), platform)
            if key in seen:
                continue
            seen.add(key)
            exes.append({"name": exe, "os": platform, "source": "discord-detectable"})
        games.append({"id": str(item.get("id", "")), "name": name, "executables": exes})
    if not games:
        raise ValueError("Nenhum jogo válido encontrado; arquivo anterior preservado")
    games.sort(key=lambda g: g["name"].casefold())
    return {
        "schema_version": 1,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": "discord-detectable",
        "count": len(games),
        "games": games,
    }

def main():
    result = normalize(fetch())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fd, path = tempfile.mkstemp(prefix=".catalog-", suffix=".json", dir=OUTPUT.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(path, OUTPUT)
    finally:
        if os.path.exists(path):
            os.unlink(path)
    print(f"Catálogo atualizado: {result['count']} jogos")

if __name__ == "__main__":
    main()
