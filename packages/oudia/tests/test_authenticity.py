import oudia


def test_oud2_import_export_empty():
    with open("./tests/empty.oud2", "r", encoding="utf-8-sig") as f:
        text = f.read()
        dia = oudia.loads(text)
        # print(dia)
        # print(dia.pprint())
    with open("./tests/empty_dumped.oud2", "w", encoding="utf-8-sig") as f:
        f.write(oudia.dumps(dia))

    assert oudia.dumps(dia) == text
