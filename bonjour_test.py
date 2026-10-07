from bonjour import displayName

def test_display_yassine():
    assert displayName("Yassine") == "Bonjour Yassine"

def test_display_vide():
    assert displayName("") == "Bonjour "