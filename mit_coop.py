from __future__ import print_function
from struct import unpack
from binascii import hexlify
from unicodedata import normalize


class OwnerInfo:
    def __init__(self, owner_info):
        self.type = int(chr(owner_info[0x00]))
        self.number = owner_info[0x02:0x0A].decode()
        self.name = normalize('NFKC', owner_info[0x10:0x20].decode('Shift_JIS'))
        self.issue_date = owner_info[0x28:0x30].decode()
        self.expiration_date = owner_info[0x30:0x38].decode()


class CoopInfo:
    def __init__(self, coop_info):
        self.number = hexlify(coop_info[:0x06])
        self.is_mealer = coop_info[0x10] == 1
        self.meal_date = hexlify(coop_info[0x12:0x15])
        self.meal_amount = int(hexlify(coop_info[0x16:0x18]))
        self.point = unpack('>I', coop_info[0x20:0x24])[0] / 10.0


class BalanceHistory:
    def __init__(self, history):
        self.date = hexlify(history[0x00:0x07])
        self.type = history[0x07]
        self.payment = hexlify(history[0x08:0x0B])
        self.balance = hexlify(history[0x0B:0x0E])


class Balance:
    def __init__(self, balance):
        self.balance = unpack('<I', balance[:0x04])[0]
        self.num_of_use = int(hexlify(balance[0x08:]))


class MitCoop:
    def __init__(self, owner_info, unk, coop_info, history, balance):
        self.owner_info = OwnerInfo(owner_info)
        self.unk = unk
        self.coop_info = CoopInfo(coop_info)
        self.histories = [BalanceHistory(bytearray(h)) for h in zip(*[iter(history)]*16)]
        self.balance = Balance(balance)
