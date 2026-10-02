from streamlit.testing.v1 import AppTest

def test_dashboard_loads_without_exceptions():
    app = AppTest.from_file(__import__('pathlib').Path(__file__).resolve().parents[1] / 'app.py').run(timeout=30)
    assert not app.exception
    assert app.title
