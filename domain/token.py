from dataclasses import dataclass
from datetime import datetime
from enum import Enum, IntEnum
from typing import List
from uuid import UUID


class Chain(Enum):
    BSC = 'bsc'
    ETH = 'eth'


@dataclass
class Token:
    id: str
    chain: Chain
    pairAddress: str
    token0Contract: str
    token0Name: str
    token0Symbol: str
    token0Supply: str


@dataclass
class CreateTokenInput:
    token_address: str
    chain: Chain
    chat_id: int


@dataclass
class UpdateTokenInput:
    group_id: str
    is_paused: bool


@dataclass
class DeleteTokenInput:
    group_id: str


@dataclass
class UpdateURLInput:
    url: str
    group_id: str
    token_id: str
