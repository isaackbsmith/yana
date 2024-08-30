from typing import Annotated
from fastapi import Depends

from yana.domain.types import YANAConfig
from yana.web.dependencies import get_config


Config = Annotated[YANAConfig, Depends(get_config)]
