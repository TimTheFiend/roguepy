from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
from components.base_component import BaseComponent
from exceptions import Impossible

if TYPE_CHECKING:
	from entity import Actor, Item


class Consumable(BaseComponent):
	parent: Item

	def get_action(self, consumer: Actor) -> Optional[actions.Action]:
		""" Try to return the action for this action. """
		return actions.ItemAction(consumer, self.parent)

	# Abstract method.
	def activate(self, action: actions.ItemAction) -> None:
		""" Invoke this items ability.

		`action` is the context for this activation.
		"""
		raise NotImplementedError()


class HealingConsumable(Consumable):
	def __init__(self, amount: int):
		self.amount = amount

	def activate(self, action: actions.ItemAction) -> None:
		consumer = action.entity
		amount_recovered = consumer.fighter.heal(self.amount)

		if amount_recovered > 0:
			self.engine.message_log.add_message(
				f"You chow down the {self.parent.name}, and recover {amount_recovered} HP! You don't know how, but it feels like you did, anyway.",
				color.health_recovered,
			)
		else:
			raise Impossible(f"Your health is already full. Weird how one can say that.")