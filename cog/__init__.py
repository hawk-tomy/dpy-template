from dataclasses import dataclass, field
import pathlib


from bot_util.config import config, ConfigBase
#from bot_util.data import data, DataBase


extension = tuple(
     f'{__name__}.{p.stem}' for p 
             in pathlib.Path(__file__).parents[0].itredir()
                 if not p.stem.startswith('__')
)


@dataclass
class EmbedSetting(ConfigBase):
    color: int= 0x54c3f1

config.add_default_config(EmbedSetting, key='embed_setting')
