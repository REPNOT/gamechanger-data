from configuration.utils import get_connection_helper_from_env
from dataPipelines.gc_db_utils.utils import check_if_table_or_view_exists
from gamechangerml import PACKAGE_PATH
import os
from functools import lru_cache

class Config:
    connection_helper = get_connection_helper_from_env()
    abbcount_json_path = os.path.join(PACKAGE_PATH, "data/features/abbcounts.json")
    agencies_csv_path = os.path.join(PACKAGE_PATH, "data/features/agencies.csv")
    graph_relations_xls_path = os.path.join(PACKAGE_PATH, "data/features/GraphRelations.xls")
    hierarchy_json_path = os.path.join(PACKAGE_PATH, "data/features/entity_hierarchy_info.json")

    @classmethod
    @lru_cache(maxsize=None)
    def does_assist_table_exist(cls):
        return check_if_table_or_view_exists(
            db_engine=cls.connection_helper.web_db_engine,
            table_or_view='gc_assists'
        )
