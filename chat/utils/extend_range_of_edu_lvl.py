
extend_map = {
    "0": "0",
    "1": "0,1,6",
    "2": "0,1,6,2,7",
    "3": "0,1,6,2,7,3,8",
    "4": "0,1,6,2,7,3,8,4,9",
    "5": "0,1,6,2,7,3,8,4,9,5"
}


def extend_range_of_edu_lvl(edu_lvl: str) -> str:
    return extend_map.get(edu_lvl, "5")
