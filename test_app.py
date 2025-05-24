from app import App
import pytest

def test_app():
    response = App.main();
    assert(len(response) > 0); 
