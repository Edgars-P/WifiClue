from typing import Optional, List, Tuple, Iterator

from wifi import WifiObservation

class Node:
  key: str
  value: WifiObservation
  next: Optional['Node']
  def __init__(self, k: str, v: WifiObservation):
    self.key = k
    self.value = v
    self.next = None

# Hastable implementācija no https://github.com/rtudip/de0918-pt-03-Edgars-P/
# Pievienoti tipi lai vieglāk strādāt
class HashTable:
  store: List[Optional[Node]] = []
  slots: int = 0
  def __init__(self, slots: int):
    self.store = []
    self.slots = slots
    # Aizpilda visus slots ar None
    for i in range(slots):
      self.store.append(None)

  # Pārtaisa key par slot index
  def _keyToIndex(self, k: str) -> int:
    return hash(k) % self.slots

  def insert(self, k: str, v: WifiObservation) -> None:
    slot = self._keyToIndex(k)
    node = self.store[slot]
    newNode = Node(k, v)
    if node == None:
      self.store[slot] = newNode
      return

    prev = node
    while node != None:
      # Ja key eksistē un signāls ir stiprāks, update value
      # Teorētiski labākais veids būtu meklēt wifi avotu apstrādājot vairākus punktus
      # bet ja ir pietiekami observations vajadzētu pietikt
      if node.key == k:
        if node.value.signalStrength > v.signalStrength:
          node.value = v
        return
      prev = node
      node = node.next
    prev.next = newNode

  def find(self, k: str) -> Optional[WifiObservation]:
    slot = self._keyToIndex(k)
    node = self.store[slot]
    while node != None:
      if node.key == k:
        return node.value
      node = node.next
    return None

  def __contains__(self, k: str) -> bool:
    return self.find(k) != None

  def remove(self, k: str) -> None:
    slot = self._keyToIndex(k)
    node = self.store[slot]
    prev = None
    while node != None:
      if node.key == k:
        if prev:
          # Ja ir vidū vai beigās, izņem un salīmē ar next
          prev.next = node.next
        else:
          # Ja ir sākumā, ieliek nākamo kā slot
          self.store[slot] = node.next
        return
      prev = node
      node = node.next

  def __iter__(self) -> Iterator:
    self.currentSlot = 0
    self.currentNode = self.store[0]
    return self

  def __next__(self) -> Tuple[str, WifiObservation]:
    # Ja ir currentNode, iet cauri visiem node šajā slot
    if self.currentNode:
      node = self.currentNode
      self.currentNode = self.currentNode.next
      return (node.key, node.value)
    # Ja nav currentNode (baidzās vai neeksistē), iet uz nāk slot
    if self.currentSlot < len(self.store) -1:
      self.currentSlot += 1
      self.currentNode = self.store[self.currentSlot]
      return self.__next__()
    # Ja nav currentNode un nav slot, beigas
    raise StopIteration
