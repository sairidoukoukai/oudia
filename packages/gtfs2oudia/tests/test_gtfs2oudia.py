from pathlib import Path

from gtfs2oudia import GTFSOuDiaConverter
from oudia import dump


from pathlib import Path

BASE_DIR = Path(__file__).parent


def test_convert():
    for gtfs_path in (BASE_DIR / "private").glob("*.zip"):
        converter = GTFSOuDiaConverter(gtfs_path)

        export_dir = Path(__file__).parent / "private" / "export" / gtfs_path.stem
        if not export_dir.exists():
            export_dir.mkdir(parents=True)
        else:
            for f in export_dir.glob("*"):
                f.unlink()

        for oudia in converter.convert_gtfs_jp_to_oudia_second():

            with open(export_dir / f"{oudia.rosen.rosenmei}.oud2", "w", encoding="utf-8-sig") as f:
                dump(oudia, f)
