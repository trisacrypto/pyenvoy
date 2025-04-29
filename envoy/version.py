"""
Defines module and package information for pyenvoy, specifically the version.
"""

# Module version and package information
__version_info__ = {
    "major": 1,
    "minor": 0,
    "micro": 1,
    "releaselevel": "final",
    "post": 0,
    "serial": 0,
}


def get_version(short: bool = False) -> str:
    """
    Prints the version.
    """
    assert __version_info__["releaselevel"] in ("alpha", "beta", "rc", "final")
    vers = ["{major}.{minor}.{micro}".format(**__version_info__)]

    if __version_info__["releaselevel"] != "final" and not short:
        vers.append(
            "-{}.{}".format(
                __version_info__["releaselevel"],
                __version_info__["serial"],
            )
        )

    if __version_info__["post"]:
        vers.append(".post{}".format(__version_info__["post"]))

    return "".join(vers)
