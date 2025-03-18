from drf_spectacular.utils import extend_schema, extend_schema_view

SCHEMA_TAGS = {
    "Country": ["Country"],
    "City": ["City"],
    "Airport": ["Airport"],
    "Route": ["Route"],
    "AirplaneType": ["Airplane Type"],
    "Airplane": ["Airplane"],
    "Flight": ["Flight"],
    "Crew": ["Crew"],
    "Order": ["Order"],
}


def schema_tags(model_name):
    return extend_schema_view(
        list=extend_schema(tags=SCHEMA_TAGS[model_name]),
        create=extend_schema(tags=SCHEMA_TAGS[model_name])
    )


def extend_schema_tags(model_name):
    return extend_schema_view(
        list=extend_schema(tags=SCHEMA_TAGS[model_name]),
        retrieve=extend_schema(tags=SCHEMA_TAGS[model_name]),
        create=extend_schema(tags=SCHEMA_TAGS[model_name]),
        update=extend_schema(tags=SCHEMA_TAGS[model_name]),
        partial_update=extend_schema(tags=SCHEMA_TAGS[model_name]),
        destroy=extend_schema(tags=SCHEMA_TAGS[model_name])
    )
