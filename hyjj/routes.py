def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.include(http_include, '/http')


def http_include(config):
    config.add_route('sendCode', '/sendCode')
    config.add_route('accountBinding', '/accountBinding')
    config.add_route('test', '/test')
