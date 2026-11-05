from domain.implant import Implant
from domain.attributes import Attribute

POWER_ARM_1 = Implant(
    name="Power Arm I",
    tier=3,
    modifiers={Attribute.STRENGTH: 1}
)

POWER_ARM_2 = Implant(
    name="Power Arm II",
    tier=4,
    modifiers={Attribute.STRENGTH: 2}
)

POWER_ARM_3 = Implant(
    name="Power Arm III",
    tier=5,
    modifiers={Attribute.STRENGTH: 3}
)

TORSO_AMPLIFIER = Implant(
    name="Torso AMPLIFIER",
    tier=2,
    modifiers={Attribute.MAX_HP: 10}
)

LEG_AMPLIFIER = Implant(
    name="Leg AMPLIFIER",
    tier=1,
    modifiers={Attribute.MAX_HP: 5}
)

ARM_AMPLIFIER = Implant(
    name="Arm AMPLIFIER",
    tier=2,
    modifiers={Attribute.MAX_HP: 5}
)

HELMET_1 = Implant(
    name="Helmet I",
    tier=1,
    modifiers={Attribute.MAX_HP: 5}
)

HELMET_2 = Implant(
    name="Helmet II",
    tier=2,
    modifiers={Attribute.MAX_HP: 10}
)