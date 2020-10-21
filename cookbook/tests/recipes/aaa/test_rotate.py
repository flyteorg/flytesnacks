from recipes.aaa import rotate


def test_fdsa():
    x = rotate.rotate(
        'https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Mandel_zoom_00_mandelbrot_set.jpg/640px-Mandel_'
        'zoom_00_mandelbrot_set.jpg')

    assert x == 'fds'


