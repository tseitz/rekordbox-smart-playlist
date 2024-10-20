import json
import shutil
import os
import xml.etree.ElementTree as ET
from sqlalchemy.orm.exc import NoResultFound
from pyrekordbox import Rekordbox6Database
from pyrekordbox.db6.smartlist import (
    SmartList,
    Condition,
    Property,
    Operator,
    LogicalOperator,
    left_bitshift,
)

from app import backup_rekordbox_md

db = Rekordbox6Database()

commit = True

created = []


def add_tag_condition_to_smart_playlist(
    condition: str,
    smart_list: SmartList,
    operator: Operator = Operator.CONTAINS,
    condition_type: Property = Property.MYTAG,
):
    if condition_type == Property.MYTAG:
        try:
            tag = db.get_my_tag(Name=condition).one()
        except NoResultFound as ex:
            print(f"{ex} -> {condition} not found")
        print(tag.Name)
    # print("Tag ID: ", tag.ID)
    # print("Tag Left Bitshift: ", left_bitshift(int(tag.ID)))
    # print("Tag Right Bitshift: ", right_bitshift(int(tag.ID)))

    if condition_type == Property.RATING:
        smart_list.add_condition(
            condition_type,
            operator,
            left_bitshift(int(tag.ID)),
            value_left=condition[0],
            value_right=condition[1],
        )
    else:
        smart_list.add_condition(
            condition_type,
            operator,
            left_bitshift(int(tag.ID)),
        )


def create_smart_playlist_from_data(
    playlist_name: str,
    logical_operator: LogicalOperator = LogicalOperator.ALL,
    main_conditions: set = [],
    negative_conditions: set = [],
    contains: list[str] = [],
    does_not_contain: list[str] = [],
    parent_playlist_id: int = None,
    playlist_type: str = "playlist",
    link: str = None,
    rating: list[str] = [],
    sequence: int = None,
):
    if playlist_type == "folder":
        if link is None:
            raise Exception("link is required for folder")
        # sub_folder = db.get_playlist(
        #     Name=playlist_name, ParentID=parent_playlist_id
        # ).one_or_none()
        # if sub_folder is None:
        #     parent_playlist = db.get_playlist(ID=parent_playlist_id)
        #     sub_folder = db.create_playlist_folder(playlist_name, parent_playlist)
        #     parent_playlist_id = sub_folder.ID

        with open(f"playlist-data/{link}", "r") as json_file:
            data = json.load(json_file)["data"]

            main_conditions.update(contains)
            add_data_to_playlist(data, parent_playlist_id, main_conditions)
            return

    smart_list = SmartList(
        logical_operator=logical_operator,
    )

    for main_condition in main_conditions:
        add_tag_condition_to_smart_playlist(main_condition, smart_list)

    # only apply this for all operator (needs to be fixed for any)
    if logical_operator == LogicalOperator.ALL:
        for negative_condition in negative_conditions:
            add_tag_condition_to_smart_playlist(
                negative_condition, smart_list, Operator.NOT_CONTAINS
            )

    for condition in contains:
        add_tag_condition_to_smart_playlist(condition, smart_list)

    for condition in does_not_contain:
        add_tag_condition_to_smart_playlist(
            condition, smart_list, Operator.NOT_CONTAINS
        )

    for condition in rating:
        add_tag_condition_to_smart_playlist(
            condition, smart_list, Operator.IN_RANGE, Property.RATING
        )

    playlist_exists = db.get_playlist(
        Name=playlist_name, ParentID=parent_playlist_id
    ).one_or_none()

    if not playlist_exists:
        created.append(playlist_name)
        db.create_smart_playlist(
            playlist_name,
            smart_list=smart_list,
            parent=parent_playlist_id,
            # seq=sequence,
        )


def add_data_to_playlist(
    data, default_playlist_id: int = None, extra_conditions: set = [], index: int = None
):
    for category in data:
        # only set index on the original parent
        # index = index if default_playlist_id is None else None
        if index is not None:
            print(f"Setting index for {category['parent']}", index)
        main_conditions = set(category["mainConditions"] + list(extra_conditions))

        if not default_playlist_id:
            default_playlist = db.get_playlist(Name="DaneDubz").one()
        else:
            default_playlist = db.get_playlist(ID=default_playlist_id)
        parent_playlist_id = default_playlist.ID

        if category["parent"]:
            existing_playlist = db.get_playlist(
                Name=category["parent"], ParentID=parent_playlist_id
            ).one_or_none()

            if existing_playlist is None:
                existing_playlist = db.create_playlist_folder(
                    category["parent"], default_playlist, index
                )
            parent_playlist_id = existing_playlist.ID

        for playlist in category["playlists"]:
            print()
            create_smart_playlist_from_data(
                playlist["name"],
                playlist["operator"],
                main_conditions,
                category.get("negativeConditions", []),
                playlist.get("contains", []),
                playlist.get("doesNotContain", []),
                playlist.get("rating", []),
                parent_playlist_id,
                playlist.get("playlistType", None),
                playlist.get("link", None),
                index,
            )


def main():
    # Read JSON file
    folder = "playlist-data"

    for index, filename in enumerate(os.listdir(folder), 5):
        if filename.endswith(".json"):
            file_path = os.path.join(folder, filename)

            with open(file_path, "r") as json_file:
                # with open("playlist-data/my-set.json", "r") as json_file:
                data = json.load(json_file)["data"]

                add_data_to_playlist(data, index=index)

    print("Created: ", created)
    if commit is True:
        backup_rekordbox_md()
        db.commit()


if __name__ == "__main__":
    main()
