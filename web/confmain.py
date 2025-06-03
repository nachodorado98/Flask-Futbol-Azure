class Config():

	SECRET_KEY="password"

class DevelopmentConfig(Config):

	DEBUG=True
	ENVIROMENT="DEV"

class ProductionConfig(Config):

	DEBUG=True
	ENVIROMENT="PRO"

config={"development":DevelopmentConfig(),
		"production":ProductionConfig()}