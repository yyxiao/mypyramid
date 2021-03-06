def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.include(mobile_include, '/mobile')


def mobile_include(config):
    config.add_route('sendCode', '/sendCode')
    config.add_route('accountBinding', '/accountBinding')
    config.add_route('riskAssess', '/riskAssess')
    config.add_route('riskSearch', '/riskSearch')
    config.add_route('riskQuestion', '/riskQuestion')
    config.add_route('myCollect', '/myCollect')
    config.add_route('productList', '/productList')
    config.add_route('productDetail', '/productDetail')
    config.add_route('productCollect', '/productCollect')
    config.add_route('productBook', '/productBook')
    config.add_route('navList', '/navList')
