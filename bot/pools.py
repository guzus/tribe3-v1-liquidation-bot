from type import Amm


def get_amms() -> list[Amm]:
    # currently hardcoded each time tribe3 adds new pools
    addresses = [
        "0x64244464a3e15990299d4106deca4f4839f3dd99",  # milady
        "0x0e9148000cc4368a5c091d85e5aa91596408594d",  # pudgy penguins
        "0x1bbc1f49497f4f1a08a93df26adfc7b0cecd95e0",  # degods
        "0xcba1f8cdd6c9d6ea71b3d88dcfb777be9bc7c737",  # captainz
        "0xd490246758b4dfed5fb8576cb9ac20073bb111dd",  # bayc
        "0x75416ee73fd8c99c1aa33e1e1180e8ed77d4c715",  # mayc
        "0xf33c2f463d5ad0e5983181b49a2d9b7b29032085",  # azuki
        "0x2396cc2b3c814609daeb7413b7680f569bbc16e0",  # crypto punks
    ]
    amms = []
    for i, addr in enumerate(addresses):
        amms.append(Amm(index=i, symbol="", address=addr, maintenance_margin_ratio="",))
    return amms
