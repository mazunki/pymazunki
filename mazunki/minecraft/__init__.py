#!/usr/bin/env python
# pkg(mazunki)/minecraft/__init__.py
from typing import Optional


class Chest:
    slots = 27
    stack_multiplier = 1
    name = "chests"

    def __init__(
        self, slots: Optional[int] = None, stack_multiplier: Optional[int] = None
    ):
        self.slots = slots or Chest.slots
        self.stack_multiplier = stack_multiplier or Chest.stack_multiplier

    def __repr__(self):
        args = []
        if self.slots != self.__class__.slots:
            args.append(f"slots={self.slots}")
        if self.stack_multiplier != self.__class__.stack_multiplier:
            args.append(f"stack_multiplier={self.stack_multiplier}")

        return f"{self.__class__.__name__}({','.join(args)})"


class DoubleChest(Chest):
    name: str = "double chests"
    slots: int = 2 * Chest.slots


class ShulkerBox(Chest):
    slots: int = 54
    name: str = "shulker boxes"


class Item:
    stack: int = 64
    name: str = "items"

    def __init__(self, stack: Optional[int] = None, name: Optional[str] = None):
        self.stack: int = stack or Item.stack
        self.name: str = name or Item.name

    def __repr__(self):
        args = []
        if self.stack != self.__class__.stack:
            args.append(f"stack={self.stack}")

        if self.name != self.__class__.name:
            args.append(f"name={self.name}")

        return f"Item({', '.join(args)})"

    def __mul__(self, other):
        if not isinstance(other, int):
            raise NotImplementedError()

        return Quantity(other, self)

    def __rmul__(self, other):
        return self.__mul__(other)


class Quantity:
    item = Item()
    chest = Chest()

    def __init__(
        self, quantity: int, item: Optional[Item] = None, chest: Optional[Chest] = None
    ):
        self.quantity = quantity
        self.item = item or self.__class__.item
        self.chest = chest or self.__class__.chest

    @property
    def total_slots(self):
        return self.in_stacks + bool(self.in_stacks[1])

    @property
    def in_stacks(self):
        return divmod(self.quantity, self.item.stack)

    @property
    def in_chests(self):
        full_stacks, extra_items = divmod(self.quantity, self.item.stack)
        full_chests, extra_slots = divmod(full_stacks, self.chest.slots)

        return full_chests, extra_slots, extra_items

    def __format__(self, fmt=""):
        if fmt in ["oneline", "boxes", "chests"]:
            fmt = "{{}} {} + {{}} slots + {{}} {}".format(
                self.chest.name, self.item.name
            )
            return fmt.format(*self.in_chests)
        elif fmt == "stacks":
            fmt = "{{}} slots + {{}} {}".format(self.item.name)
            return fmt.format(*self.in_stacks)
        elif fmt == "qty":
            fmt = "{{}} {}".format(self.item.name)
            return fmt.format(self.quantity)
        else:
            return "\n".join(
                (
                    self.__format__("qty"),
                    self.__format__("stacks"),
                    self.__format__("boxes"),
                )
            )

    def __str__(self):
        return self.__format__()

    def __repr__(self):
        args = [f"quantity={self.quantity}"]
        if self.item is not self.__class__.item:
            args.append(f"item={self.item}")
        if self.chest is not self.__class__.chest:
            args.append(f"chest={self.chest}")
        return f"{self.__class__.__name__}({', '.join(args)})"

    def __matmul__(self, other):
        if not isinstance(other, Chest):
            return NotImplementedError()

        return Quantity(self.quantity, self.item, other)


def test():
    for qty in map(Quantity, (1000, 1727, 1728, 1729, 2000, 3000)):
        print(repr(qty))
