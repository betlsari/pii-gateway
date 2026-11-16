from pii_gateway.models import Category, Finding

def test_finding_alanlari():
    f = Finding(Category.TCKN, 24, 35, "10000000146", 1.0)
    assert f.start == 24
    assert f.end == 35
    assert f.text == "10000000146"
    assert f.category == Category.TCKN
    assert f.category.value == "TCKN"