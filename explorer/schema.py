from django.core.cache import cache

from explorer.app_settings import (
    ENABLE_TASKS, EXPLORER_ASYNC_SCHEMA, EXPLORER_CONNECTIONS, EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES,
    EXPLORER_SCHEMA_INCLUDE_TABLE_PREFIXES, EXPLORER_SCHEMA_INCLUDE_VIEWS,
)
from explorer.tasks import build_schema_cache_async
from explorer.utils import get_valid_connection, InvalidExplorerConnectionException


# These wrappers make it easy to mock and test
def _get_includes():
    return EXPLORER_SCHEMA_INCLUDE_TABLE_PREFIXES


def _get_excludes():
    return EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES


def _include_views():
    return EXPLORER_SCHEMA_INCLUDE_VIEWS is True


def do_async():
    return ENABLE_TASKS and EXPLORER_ASYNC_SCHEMA


def _include_table(t):
    if _get_includes() is not None:
        return any([t.startswith(p) for p in _get_includes()])
    return not any([t.startswith(p) for p in _get_excludes()])


def connection_schema_cache_key(connection_alias):
    return f"_explorer_cache_key_{connection_alias}"


def connection_schema_json_cache_key(connection_alias):
    return f"_explorer_cache_key_json_{connection_alias}"


def transform_to_json_schema(schema_info):
    json_schema = {}
    for table_name, columns in schema_info:
        json_schema[table_name] = []
        for column_name, _ in columns:
            json_schema[table_name].append(column_name)
    return json_schema


def schema_json_info(connection_alias):
    key = connection_schema_json_cache_key(connection_alias)
    ret = cache.get(key)
    if ret:
        return ret
    try:
        si = schema_info(connection_alias) or []
    except InvalidExplorerConnectionException:
        return []
    json_schema = transform_to_json_schema(si)
    cache.set(key, json_schema)
    return json_schema


def schema_info(connection_alias):
    key = connection_schema_cache_key(connection_alias)
    ret = cache.get(key)
    if ret:
        return ret
    if do_async():
        build_schema_cache_async.delay(connection_alias)
    else:
        return build_schema_cache_async(connection_alias)


def clear_schema_cache(connection_alias):
    key = connection_schema_cache_key(connection_alias)
    cache.delete(key)

    key = connection_schema_json_cache_key(connection_alias)
    cache.delete(key)


def build_schema_info(connection_alias):
    """
        Construct schema information via engine-specific queries of the
        tables in the DB.

        :return: Schema information of the following form,
                 sorted by db_table_name.
            [
                ("db_table_name",
                    [
                        ("db_column_name", "DbFieldType"),
                        (...),
                    ]
                )
            ]

        """
    connection = get_valid_connection(connection_alias)
    ret = []
    with connection.cursor() as cursor:
        tables_to_introspect = connection.introspection.table_names(
            cursor, include_views=_include_views()
        )

        for table_name in tables_to_introspect:
            if not _include_table(table_name):
                continue
            td = []
            table_description = connection.introspection.get_table_description(
                cursor, table_name
            )
            for row in table_description:
                column_name = row[0]
                try:
                    field_type = connection.introspection.get_field_type(
                        row[1], row
                    )
                except KeyError:
                    field_type = "Unknown"
                td.append((column_name, field_type))
            ret.append((table_name, td))
    return ret


def build_async_schemas():
    if do_async():
        for c in EXPLORER_CONNECTIONS:
            schema_info(c)
