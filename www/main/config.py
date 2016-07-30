import os.path


class BasicConfig:
    BASE_DIR = os.path.dirname(os.path.abspath(__name__))

    # Twitter (auth_api).
    CONS_KEY = "KLgeXShNvyawbCF68xIQnxQ7I"    # Public api.
    CONS_SECRET = "m9tqmRVGV2kMSa2Fp6ges4QpTd4cauhXlIi1sb19OclUO2OYpv"    # Pub
    TOKEN_KEY = '745349279326281730-jK28eboGXFXeSUU4toHhugXJA4aoMVd'
    TOKEN_SECRET = '7vLVLcnH6YFBGTplllKxH4INZYXSbbTWyk3KsQwsjPoTY'


class DevConfig(BasicConfig):
    DEBUG = True

    # Twitter (test_server_api).
    CONS_KEY = "ElBHq7mwPAIToQDPsuWd3HZia"      # Test api.
    CONS_SECRET = "6kJBDAtaKUdd2FSw7HMXovVyY3HEIWwMatk56Mm63Tn3ThuT6i"
    TOKEN_KEY = '745349279326281730-hAApOEvRWdlybrGDr8DIhYvMflPKWn4'
    TOKEN_SECRET = 'aC7y5V2TGBewvPSmw6N8kslH2werkCMYa5lQSrtafrMcT'


config = {
    "BASIC_CONF": BasicConfig,
    "DEV_CONF": DevConfig,
    "default": BasicConfig
}
