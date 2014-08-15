from mobileparser.unica import Unica


def setup_module(module):
    unica_parser = Unica()
    with ('resources/assari.html', 'r') as my_file:
        assari = my_file.read()
    with ('resources/delipharma.html', 'r') as my_file:
        delipharma = my_file.read()


class TestUnica:

    def test_assaris_foods_not_empty(self):
        assert unica_parser.assert_foods_not_empty(assari)

    def test_delipharmas_foods_are_empty(self):
        assert not unica_parser.assert_foods_not_empty(delipharma)
