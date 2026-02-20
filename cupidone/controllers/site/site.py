from cupidone.actions import Commands

from ..composite import CompositeController

from .internal import *


class SiteController(CompositeController):
    def __init__(self, fm, tm):
        cs = [
            SiteBuildController(fm, tm)
        ]
        super().__init__(fm, tm, cs)

    def keys(self):
        return [Commands.SITE]


__all__ = ["SiteController"]