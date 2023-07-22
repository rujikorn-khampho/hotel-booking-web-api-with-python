from functools import reduce
from typing import Union, Dict, Any


def get_value_from_nested_dict(
        dictionary: Union[Dict[str, Any], Any],
        keys: str,
        default: Any = None,
) -> Any:
    return reduce(
        lambda d, key: d.get(key, default)
        if isinstance(d, dict) else default, keys.split('.'), dictionary
    )
