import sqlite3


def get_all(query):
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row

        result = []

        for item in connection.execute(query).fetchall():
            result.append(item)

        return result


def get_one(query):
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(query).fetchone()

        if result is None:
            return None
        else:
            return result


def search_by_cast(act1, act2):
    query = f"""SELECT netflix.cast FROM netflix WHERE netflix.cast LIKE '%{act1}%' AND netflix.cast LIKE '%{act2}%'"""

    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row

        result = get_all(query)
        cast = []
        set_cast = set()

        for item in result:
            for act in item['cast'].split(', '):
                cast.append(act)

        for act in cast:
            if cast.count(act) > 2:
                set_cast.add(act)

        set_cast.remove(act1)
        set_cast.remove(act2)

        return list(set_cast)


def get_title_by_values(title_type, release_year, listed_in):
    query = f"""
    SELECT title, description 
    FROM netflix
    WHERE 'type' = '{title_type}' 
    AND release_year = '{release_year}' 
    AND listed_in = '%{listed_in}%'
    """

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'description': item['description'],
            }
        )

    return result
