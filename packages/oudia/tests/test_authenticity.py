"""This module tests the reproducibility by comparing loaded then dumped data"""

import oudia
import sys
from pathlib import Path

base_dir = Path(__file__).parent


def test_oud2_import_export_empty():
    with open(base_dir / "empty.oud2", "r", encoding="utf-8-sig") as f:
        text = f.read()
        dia = oudia.loads(text)
        # print(dia)
        # print(dia.pprint())
    with open(base_dir / "empty_dumped.oud2", "w", encoding="utf-8-sig") as f:
        f.write(oudia.dumps(dia))

    assert oudia.dumps(dia) == text


def test_oud2_import_export_private():
    for artifact in Path(base_dir / "private").glob("**/*.dumped.oud*"):
        artifact.unlink()

    for oud in Path(base_dir / "private").glob("*.oud*"):
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

            with open(oud.with_suffix(".dumped" + oud.suffix + ".pprint.txt"), "w", encoding="utf-8") as sys.stdout:
                dia.pprint()

            with open(oud.with_suffix(".dumped" + oud.suffix + ".repr.py"), "w", encoding="utf-8") as sys.stdout:
                print(repr(dia))

        assert dumped == text, f"Re-exported file is not the same as original: {oud}"


def test_oud_import_export_private_shift_jis():
    for artifact in Path(base_dir / "private/oud").glob("**/*.dumped.oud*"):
        artifact.unlink()

    for oud in Path(base_dir / "private/oud").glob("*.oud*"):
        try:
            with open(oud, "r", encoding="shift-jis") as f:
                text = f.read()
                try:
                    dia = oudia.loads(text)
                except Exception:
                    print(oud)
                    continue
        except Exception:
            print(oud)
            raise

        try:
            dumped = oudia.dumps(dia)
        except Exception:
            print(oud)
            continue

        if dumped != text:
            with open(oud.with_suffix(".dumped" + oud.suffix), "w", encoding="shift-jis") as f:
                f.write(oudia.dumps(dia))

            with open(oud.with_suffix(".dumped" + oud.suffix + ".pprint.txt"), "w", encoding="utf-8") as sys.stdout:
                dia.pprint()

            with open(oud.with_suffix(".dumped" + oud.suffix + ".repr.py"), "w", encoding="utf-8") as sys.stdout:
                print(repr(dia))

        assert dumped == text, f"Re-exported file is not the same as original: {oud}"
