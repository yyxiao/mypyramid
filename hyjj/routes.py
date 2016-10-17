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
    config.add_route('fundList', '/fundList')
    config.add_route('fundDetail', '/fundDetail')
    config.add_route('fundCollect', '/fundCollect')
    config.add_route('fundBook', '/fundBook')
    config.add_route('test', '/test')
