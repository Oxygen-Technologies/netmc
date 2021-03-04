# coding=utf-8
from collections import namedtuple
from .base_behavior import BaseBehavior
from .utils import CompFactory

ItemData = namedtuple('ItemData', 'name count aux_value')


def _format_item_data_to_netease(item_data):
    # type: (ItemData) -> dict
    return {
        'itemName': item_data.name,
        'count': item_data.count,
        'auxValue': item_data.aux_value
    }


class Item(BaseBehavior):
    def __init__(self, uid):
        super(Item, self).__init__(uid)

    def spawn_item_to_inventory(self, item_data):
        # type: (ItemData) -> None
        CompFactory.CreateItem(self._uid).SpawnItemToPlayerInv(_format_item_data_to_netease(item_data), self._uid)
