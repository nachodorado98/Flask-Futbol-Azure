import os

class Config():

	SECRET_KEY="password"

class DevelopmentConfig(Config):

	DEBUG=True
	ENVIROMENT="dev"

class ProductionConfig(Config):

	DEBUG=True
	ENVIROMENT=os.environ.get("AZURE_NAME_CONTAINER") # Nombre del contenedor

config={"development":DevelopmentConfig(),
		"production":ProductionConfig()}