from typing import Annotated
from fastapi import Depends

from yana.domain.types import YANAConfig
from yana.utils.config import get_config, get_test_config


Config = Annotated[YANAConfig, Depends(get_config)]

TestConfig = Annotated[YANAConfig, Depends(get_test_config)]
