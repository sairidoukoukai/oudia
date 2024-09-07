import oudia

from pathlib import Path


def test_readme():
    # TODO: make sairibus authentic OuDia
    base_dir = Path(__file__).parent
    with open(base_dir / "sairibus.oud", "r", encoding="shift-jis") as f:
        dia = oudia.load(f)
        print(dia.file_type)
        for eki in dia.rosen.eki_list:
            print(eki.ekimei)

    with open(base_dir / "meronking_line.oud2", "r", encoding="utf-8-sig") as f:
        dia = oudia.load(f)
        print(dia.file_type)
        print(dia.rosen)

    with open(base_dir / "meronking_line_dumped.oud2", "w", encoding="utf-8-sig") as f:
        dumped_str = oudia.dumps(dia)
        f.write(dumped_str)
