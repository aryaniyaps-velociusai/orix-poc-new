from decouple import config


class DefaultConfig:
    # PORT = config("PORT")

    # AWS_REGION = config("AWS_REGION")

    # OPENAI_API_TYPE = config("OPENAI_API_TYPE")
    # OPENAI_API_BASE = config("OPENAI_API_BASE")
    # OPENAI_API_KEY = config("OPENAI_API_KEY")

    # OPENAI_API_BASE_2 = config("OPENAI_API_BASE_2")
    # OPENAI_API_KEY_2 = config("OPENAI_API_KEY_2")

    # # GPT 4
    # OPENAI_API_VERSION = config("OPENAI_API_VERSION")
    # OPENAI_DEPLOYMENT_NAME = config("OPENAI_DEPLOYMENT_NAME")
    # OPENAI_MODEL_NAME = config("OPENAI_MODEL_NAME")

    # # GPT 3.5 Turbo 16k
    # OPENAI_DEPLOYMENT_NAME_35 = config("OPENAI_DEPLOYMENT_NAME_35")
    # OPENAI_MODEL_NAME_35 = config("OPENAI_MODEL_NAME_35")
    # OPENAI_API_VERSION_35 = config("OPENAI_API_VERSION_35")

    # APP_ID = config("MICROSOFT_APP_ID")
    # APP_SECRET = config("MICROSOFT_APP_PASSWORD")
    # TENANT_ID = config("TENANT_ID")

    # TEMP_PATH = "/tmp"

    DATABASE_URI = config("DATABASE_URI")
    KEY = config("DATABASE_KEY")
    DATABASE_ID = config("DATABASE_ID")
    CONTAINER_ID = config("CONTAINER_ID")
    PARTITION_ENV = config("PARTITION_ENVIRONMENT_KEY")

    ENVIRONMENT = config(
        "ENV"
    )  # environment in which the script is running e.g. local, dev, qa, prod

    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT_1 = config(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT_1"
    )
    AZURE_DOCUMENT_INTELLIGENCE_KEY_1 = config("AZURE_DOCUMENT_INTELLIGENCE_KEY_1")

    MAX_PAGES_PROCESSED_PER_PDF = config("MAX_PAGES_PROCESSED_PER_PDF", default=40)

    # OPERATOR_STAGING_LOCATION = config("OPERATOR_STAGING_LOCATION", "", cast=str)
    # # add operator's email in comma separated values in app setting: test@gmail.com, test2@gmail.com
    # OPERATORS = config(
    #     "OPERATORS", "", cast=lambda v: [s.strip() for s in v.split(",") if s.strip()]
    # )
    # OPERATOR_MODE = config("OPERATOR_MODE", True, cast=bool)

    # SENDGRID_API_KEY = config("SENDGRID_API_KEY")

    # MAX_CONCURRENT_WORKERS = config("MAX_CONCURRENT_WORKERS", 15, cast=int)

    # ONESIZER_TEMPLATE_URL = config("ONESIZER_TEMPLATE_URL")
