from logging import Logger

from model.oapen_types import OapenSuggestion


def table_exists(connection, table):
    cursor = connection.cursor
    cursor.execute(
        "select exists(select * from oapen_suggestions.tables where table_name=%s)",
        (table),
    )

    res = cursor.fetchone()[0]
    cursor.close()
    return res


def add_suggestion(connection, suggestion: OapenSuggestion) -> None:
    cursor = connection.cursor()

    query = """
            INSERT INTO oapen_suggestions.suggestions VALUES (%s, %s, %s)
        """

    try:
        cursor.execute(query, suggestion)
    except Exception as ex:
        Logger.exception(ex)
    finally:
        cursor.close()


def add_many_suggestions(connection, suggestions) -> None:
    cursor = connection.cursor()

    args_str = ",".join(
        cursor.mogrify("(%s,%s,%s::suggestion[])", x).decode("utf-8")
        for x in suggestions
    )

    query = f"""
        INSERT INTO oapen_suggestions.suggestions VALUES {args_str}
    """

    try:
        cursor.execute(query)
    except Exception as ex:
        Logger.exception(ex)
    finally:
        cursor.close()
