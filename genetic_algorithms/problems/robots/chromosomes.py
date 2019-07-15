import attr
from itertools import product
import numpy as np


@attr.s(kw_only=True)
class Motor:
    type_: str = attr.ib()
    power: int = attr.ib()
    valid_motor_types = ["step", "servo"]
    valid_power_values = [5, 9, 12, 24]

    @type_.validator
    def valid_motor_type(self, attribute, value):
        if value not in self.valid_motor_types:
            raise ValueError(
                f"`{value}` is an invalid motor type. Valid motor types are {self.valid_motor_types}"
            )

    @power.validator
    def valid_power(self, attribute, value):
        if value not in self.valid_power_values:
            raise ValueError(
                f"`{value}` is an invalid power value. Valid power values are {self.valid_power_values}"
            )

    @property
    def possible_motors(self):
        return list(product(self.valid_motor_types, self.valid_power_values))

    @property
    def weight(self):
        # TODO: improve the association between types and weights
        weights = dict(zip(self.valid_motor_types, [240, 63]))
        return weights[self.type_]

    def as_binary(self):
        # Width is set to 3 because a motor is encoded in 3 bits
        return np.binary_repr(self.possible_motors.index((self.type_, self.power)), 3)

    @classmethod
    def from_binary(cls, motor):
        # TODO: currently a hack, check how to access property from classmethod
        possible_motors = list(product(cls.valid_motor_types, cls.valid_power_values))
        possible_motor_index = int(motor, 2)
        motor = possible_motors[possible_motor_index]
        type_, power = motor
        return cls(type_=type_, power=power)


# %%
@attr.s(kw_only=True)
class PowerSource:
    type_: str = attr.ib()
    power: int = attr.ib()
    valid_power_source_types = [
        "nickel_cadmium",
        "lithium_ion",
        "solar_panel",
        "fusion_reactor",
    ]
    valid_power_values = [12, 24]

    @type_.validator
    def valid_power_source_type(self, attribute, value):
        if value not in self.valid_power_source_types:
            raise ValueError(
                f"`{value}` is an invalid power source type. Valid power source types are {self.valid_power_source_types}"
            )

    @power.validator
    def valid_power(self, attribute, value):
        if value not in self.valid_power_values:
            raise ValueError(
                f"`{value}` is an invalid power value. Valid power values are {self.valid_power_values}"
            )

    @property
    def weight(self):
        weights = dict(zip(self.valid_power_source_types, [220, 200, 400, 1000]))
        return weights[self.type_]

    @property
    def possible_power_sources(self):
        return list(product(self.valid_power_source_types, self.valid_power_values))

    def as_binary(self):
        # Width is set to 3 because a motor is encoded in 3 bits
        return np.binary_repr(
            self.possible_power_sources.index((self.type_, self.power)), 3
        )

    @classmethod
    def from_binary(cls, motor):
        # TODO: currently a hack, check how to access property from classmethod
        possible_power_sources = list(
            product(cls.valid_power_source_types, cls.valid_power_values)
        )
        possible_power_source_index = int(motor, 2)
        power_source = possible_power_sources[possible_power_source_index]
        type_, power = power_source
        return cls(type_=type_, power=power)


# %%
@attr.s(kw_only=True)
class Robot:
    motor = attr.ib()
    power_source = attr.ib()

    @property
    def weight(self):
        return self.motor.weight + self.power_source.weight

    @property
    def specific_power(self):
        """range is defined as the distance the robot can travel given its weight and power source capacity.

        Returns:
            float -- the ratio of the robot's power source capacity and its total weight
        """
        # https://en.wikipedia.org/wiki/Power-to-weight_ratio#Power-to-weight_(specific_power)
        return self.power_source.power / self.weight

    def as_binary(self):
        return f"{self.motor.as_binary()}{self.power_source.as_binary()}"

    @classmethod
    def from_binary(cls, robot):
        motor = robot[:3]
        power_source = robot[3:]
        return cls(
            motor=Motor.from_binary(motor),
            power_source=PowerSource.from_binary(power_source),
        )

