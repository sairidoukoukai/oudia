import inspect

import oudia


def test_file_type_app_comment_after_file_type():
    """OuDia.2・OuDia.3はアプリコメントをファイル形式の直後に置く。"""
    text = inspect.cleandoc(
        """
            FileType=OuDia.2
            FileTypeAppComment=OuDia Ver. 0.02.03
            Rosen.
            Rosenmei=阪急宝塚線
            .
            DispProp.
            .
        """
    )
    dia = oudia.loads(text)

    assert dia.file_type_app_comment == "OuDia Ver. 0.02.03"
    assert dia.file_type_app_comment_after_file_type is True
    assert oudia.dumps(dia) == text + "\n"


def test_file_type_app_comment_at_end():
    """OuDiaSecondはアプリコメントを末尾に置く。"""
    text = inspect.cleandoc(
        """
            FileType=OuDiaSecond.1.14
            Rosen.
            Rosenmei=再履バス
            .
            DispProp.
            .
            FileTypeAppComment=OuDiaSecondV2 Ver. 2.06.14
        """
    )
    dia = oudia.loads(text)

    assert dia.file_type_app_comment == "OuDiaSecondV2 Ver. 2.06.14"
    assert dia.file_type_app_comment_after_file_type is False
    assert oudia.dumps(dia) == text + "\n"
