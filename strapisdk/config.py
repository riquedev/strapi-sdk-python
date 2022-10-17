from dotenv import dotenv_values

env = dotenv_values('.env')
STRAPI_API_URL = env.get('STRAPI_API_URL')
STRAPI_IDENTIFIER = env.get('STRAPI_IDENTIFIER')
STRAPI_PASSWORD = env.get('STRAPI_PASSWORD')
STRAPI_TEST_COLLECTION = env.get('STRAPI_TEST_COLLECTION')
STRAPI_TEST_COLLECTION_ID = int(env.get('STRAPI_TEST_COLLECTION_ID', '1'))