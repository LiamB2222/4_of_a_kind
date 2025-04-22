from enum import Enum
from treys import Card as TreyCard


class Card(Enum):
    # Aces
    AceHearts = TreyCard.new('Ah')
    AceSpades = TreyCard.new('As')
    AceClubs = TreyCard.new('Ac')
    AceDiamonds = TreyCard.new('Ad')

    # Twos
    TwoHearts = TreyCard.new('2h')
    TwoSpades = TreyCard.new('2s')
    TwoClubs = TreyCard.new('2c')
    TwoDiamonds = TreyCard.new('2d')

    # Threes
    ThreeHearts = TreyCard.new('3h')
    ThreeSpades = TreyCard.new('3s')
    ThreeClubs = TreyCard.new('3c')
    ThreeDiamonds = TreyCard.new('3d')

    # Fours
    FourHearts = TreyCard.new('4h')
    FourSpades = TreyCard.new('4s')
    FourClubs = TreyCard.new('4c')
    FourDiamonds = TreyCard.new('4d')

    # Fives
    FiveHearts = TreyCard.new('5h')
    FiveSpades = TreyCard.new('5s')
    FiveClubs = TreyCard.new('5c')
    FiveDiamonds = TreyCard.new('5d')

    # Sixes
    SixHearts = TreyCard.new('6h')
    SixSpades = TreyCard.new('6s')
    SixClubs = TreyCard.new('6c')
    SixDiamonds = TreyCard.new('6d')

    # Sevens
    SevenHearts = TreyCard.new('7h')
    SevenSpades = TreyCard.new('7s')
    SevenClubs = TreyCard.new('7c')
    SevenDiamonds = TreyCard.new('7d')

    # Eights
    EightHearts = TreyCard.new('8h')
    EightSpades = TreyCard.new('8s')
    EightClubs = TreyCard.new('8c')
    EightDiamonds = TreyCard.new('8d')

    # Nines
    NineHearts = TreyCard.new('9h')
    NineSpades = TreyCard.new('9s')
    NineClubs = TreyCard.new('9c')
    NineDiamonds = TreyCard.new('9d')

    # Tens
    TenHearts = TreyCard.new('Th')
    TenSpades = TreyCard.new('Ts')
    TenClubs = TreyCard.new('Tc')
    TenDiamonds = TreyCard.new('Td')

    # Jacks
    JackHearts = TreyCard.new('Jh')
    JackSpades = TreyCard.new('Js')
    JackClubs = TreyCard.new('Jc')
    JackDiamonds = TreyCard.new('Jd')

    # Queens
    QueenHearts = TreyCard.new('Qh')
    QueenSpades = TreyCard.new('Qs')
    QueenClubs = TreyCard.new('Qc')
    QueenDiamonds = TreyCard.new('Qd')

    # Kings
    KingHearts = TreyCard.new('Kh')
    KingSpades = TreyCard.new('Ks')
    KingClubs = TreyCard.new('Kc')
    KingDiamonds = TreyCard.new('Kd')
