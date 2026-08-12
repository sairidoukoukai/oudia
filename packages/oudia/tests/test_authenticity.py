"""This module tests the reproducibility by comparing loaded then dumped data"""

import sys
from pathlib import Path

import pytest

import oudia

base_dir = Path(__file__).parent

INDEXED_NODE_LIST_FILES = {
    "fukuitetsudo_0604.oud",
    "hankyu_takarazuka_0208.oud",
    "hsb_07.oud",
    "jr_narasen_0603.oud",
    "kansai_kisei_0601.oud",
    "nankai_0511.oud",
    "nankai_kouya_0510.oud",
    "nishitetsumiyajidake_0703.oud",
    "toyama_lightrail_0604.oud",
}
"""OuDia 0.02〜0.04が書いた`Eki[]=23`・`Eki[0].`の形の配列を使うファイル。

この形はまだ読めないため、丸ごと除いてある。読めるようになったらこの集合を空にする。
"""


def dumped_artifact_paths(oud: Path) -> tuple[Path, Path, Path]:
    """食い違ったときに残す、書き出し結果とその内訳の置き場。"""
    dumped = oud.with_suffix(".dumped" + oud.suffix)
    return dumped, Path(str(dumped) + ".pprint.txt"), Path(str(dumped) + ".repr.py")


def assert_round_trip(oud: Path, encoding: str) -> None:
    """読み込んで書き出した結果が元のファイルと一致することを確かめます。"""
    text = oud.read_text(encoding=encoding)
    dia = oudia.loads(text)
    dumped = oudia.dumps(dia)

    if dumped != text:
        dumped_path, pprint_path, repr_path = dumped_artifact_paths(oud)
        dumped_path.write_text(dumped, encoding=encoding)
        with open(pprint_path, "w", encoding="utf-8") as sys.stdout:
            dia.pprint()
        sys.stdout = sys.__stdout__
        repr_path.write_text(repr(dia), encoding="utf-8")

    assert dumped == text, f"Re-exported file is not the same as original: {oud}"


def clean_artifacts(directory: Path) -> None:
    """前回残した書き出し結果を消します。"""
    for artifact in directory.glob("**/*.dumped.oud*"):
        artifact.unlink()


def collect(directory: Path) -> list[Path]:
    """丸め込みを試すファイルを集めます。"""
    return sorted(p for p in directory.glob("*.oud*") if ".dumped" not in p.name)


def test_oud2_import_export_empty():
    text = (base_dir / "empty.oud2").read_text(encoding="utf-8-sig")
    dia = oudia.loads(text)

    assert oudia.dumps(dia) == text


@pytest.mark.parametrize("oud", collect(base_dir / "private"), ids=lambda p: p.name)
def test_oud2_import_export_private(oud: Path):
    clean_artifacts(base_dir / "private")
    assert_round_trip(oud, "utf-8-sig")


@pytest.mark.parametrize("oud", collect(base_dir / "private/ouds"), ids=lambda p: p.name)
def test_oud_import_export_private_cp932(oud: Path):
    if oud.name in INDEXED_NODE_LIST_FILES:
        pytest.skip("OuDia 0.02〜0.04の添字付き配列は未対応")

    clean_artifacts(base_dir / "private/ouds")
    assert_round_trip(oud, "cp932")
