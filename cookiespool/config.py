# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = 'foobared'

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'zlhunt': 'ZlHuntCookiesGenerator'
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'zlhunt': 'ZlHuntValidTester'
}

TEST_URL_MAP = {
    'zlhunt': 'https://sou.zhaopin.com/?jl=538&kw=python&kt=3&sf=0&st=0'
}

# 产生器和验证器循环周期
CYCLE = 120

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5000

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = False
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = False
# API接口服务
API_PROCESS = True

# 要爬取的URL
URL = 'https://sou.zhaopin.com/?jl=538&kw=python&kt=3&sf=0&st=0&p='