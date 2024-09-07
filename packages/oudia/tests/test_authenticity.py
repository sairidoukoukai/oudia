import oudia
from pathlib import Path


def test_oud2_import_export_empty():
    with open("./tests/empty.oud2", "r", encoding="utf-8-sig") as f:
        text = f.read()
        dia = oudia.loads(text)
        # print(dia)
        # print(dia.pprint())
    with open("./tests/empty_dumped.oud2", "w", encoding="utf-8-sig") as f:
        f.write(oudia.dumps(dia))

    assert oudia.dumps(dia) == text


def test_oud2_import_export_private():
    for oud in Path("./tests/private").glob("*.oud*"):
        if ".dumped.oud" in oud.name:
            oud.unlink()
            continue

        with open(oud, "r", encoding="utf-8-sig") as f:
            text = f.read()
            try:
                dia = oudia.loads(text)
            except Exception:
                print(oud)
                continue

        try:
            dumped = oudia.dumps(dia)
        except Exception:
            print(oud)
            continue

        if dumped != text:
            with open(oud.with_suffix(".dumped" + oud.suffix), "w", encoding="utf-8-sig") as f:
                f.write(oudia.dumps(dia))
        assert dumped == text
