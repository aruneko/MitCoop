#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function
import nfc
import mit_coop


def on_connect(tag):
    # System Codeの指定とPollingの開始
    system_code = 0xfe00
    idm, pmm = tag.polling(system_code=system_code)
    tag.idm, tag.pmm, tag.sys = idm, pmm, system_code

    # Service CodeとBlock Codeをリスト化
    service_codes = [nfc.tag.tt3.ServiceCode(c >> 6, c & 0x3f) for c in [0x1A8B, 0x434B, 0x50CB, 0x50CF, 0x50D7]]
    block_ranges = [range(i) for i in [4, 3, 6, 10, 1, 1]]
    block_codes = [map(lambda i: nfc.tag.tt3.BlockCode(i, service=0), r) for r in block_ranges]

    # リストからごそっと引っ張ってくる
    results = [tag.read_without_encryption([sc], bc) for sc, bc in zip(service_codes, block_codes)]
    owner_info, unk, coop_info, history, balance = results

    # パースして表示
    card = mit_coop.MitCoop(owner_info, unk, coop_info, history, balance)

    print("-----カード情報-----")
    print("種別:", "学生" if card.owner_info.type == 0 else "職員")
    print("氏名:", card.owner_info.name)
    print("学籍番号:", card.owner_info.number)
    print("発行日:", card.owner_info.issue_date)
    print("有効期限:", card.owner_info.expiration_date)

    print("-----生協情報-----")
    print("生協利用者番号:", card.coop_info.number)
    print("ミーラー:", card.coop_info.is_mealer)
    print("ミールカード最終利用日:", card.coop_info.meal_date)
    print("ミールカード利用額:", card.coop_info.meal_amount)
    print("ポイント:", card.coop_info.point)

    print("-----利用履歴-----")
    for h in card.histories:
        print("利用日時:", h.date)
        print("利用分類:", "支払い" if h.type == 5 else "チャージ")
        print("利用金額:", h.payment)
        print("残高:", h.balance)

    print("-----プリペイド情報-----")
    print("プリペイド残高:", card.balance.balance)
    print("プリペイド利用回数:", card.balance.num_of_use)


def main():
    with nfc.ContactlessFrontend('usb') as clf:
        clf.connect(rdwr={'on-connect': on_connect})


main()
