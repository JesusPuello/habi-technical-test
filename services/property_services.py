from utils import my_sql_connector, property_filters, status_mapper
from typing import Dict


def find_available_houses(args: Dict[str, any] = {}):
    db = my_sql_connector.DatabaseHandler()
    select_query = """
        select * from(
            select 
            p.id, 
            p.address, 
            p.city, 
            p.price, 
            p.description, 
            p.year,
            SUBSTRING_INDEX( GROUP_CONCAT(CAST(sh.status_id AS CHAR) ORDER BY sh.update_date desc), ',', 1 ) AS status_id
            from property p 
            inner join status_history sh 
            on sh.property_id = p.id 
            group by p.id
        ) as information
        where status_id in ('3', '4', '5'){}
    """.format(
        conditional_where(args)
    )
    db.cursor.execute(select_query)
    data = db.cursor.fetchall()
    db.close_all()
    return filter_incongruent_data(map_data(data))


def filter_incongruent_data(data: list) -> list:
    return list(
        filter(lambda h: h.get("address", False) and h.get("city", False), data)
    )


def map_data(data: list) -> list:
    return list(
        map(
            lambda h: {
                "address": h[1],
                "city": h[2],
                "status": status_mapper.DB_STATUS_MAPPER.get(h[6]),
                "price": h[3],
                "description": h[4],
            },
            data,
        )
    )


def conditional_where(args: Dict[str, any]) -> str:
    extra_filters = ""
    for arg in args:
        arg_type = property_filters.EXPECTED_ARGS.get(arg)
        extra_filters += (
            f" and {arg} = '{args.get(arg)}'"
            if arg_type == str
            else f" and {arg} = {args.get(arg)}"
        )

    return extra_filters
