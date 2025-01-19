from typing import List
import networkx as nx
import json as json

class UserAvail:
    def __init__(self, js):
        self.email = "munce@ubc.ca"
        self.blocks = [1, 2, 3, 4, 5]
        self.max_blocks = 2
        self.__dict__ = json.loads(js)

class Slot:
    def __init__(self, js):
        self.name = "L2A"
        self.slotId = 2
        self.numMembers = 3
        self.startBlock = 2
        self.endBlock = 4
        self.__dict__ = json.loads(js)

class MemberSlot:
    """
    Sample MemberSlot:
    email: "munce@ubc.ca",
    slot_id: 2,
    prefer_level: 1

    prefer_level is 1 for "Perfectly available", 2 for "Prefer not"
    """
    def __init__(self, email: str, slot_id: int, prefer_level: int):
        self.email = email
        self.slot_id = slot_id
        self.prefer_level = prefer_level

class MemberAvail:
    def __init__(self, email: str, avail_slots: List[MemberSlot], max_blocks: int):
        self.email = email
        self.avail_slots = avail_slots
        self.max_blocks = max_blocks



def match_avails_to_slots(avails: List[UserAvail], slots: List[int]) -> List[MemberAvail]:
    """
    Change a block array to available slots.

    Sample input:
    [
        {
            "email": "munce@ubc.ca",
            "blocks": [1, 2, 3, 4, 5],
            "max_blocks": 2
        }
    ]
    [
        {
            "name": "L2A",
            "slotId": 2,
            "numMembers": 3,
            "startBlock": 2,
            "endBlock": 4
        }
    ]

    Sample output:
    [
        {
            "email": "munce@ubc.ca",
            "avail_slots": [
                {
                    "email": "munce@ubc.ca",
                    "slot_id": 2,
                    "prefer_level": 2
                }
            ],
            "max_blocks": 2
        }
    ]
    """
    return []


def blocks_to_array(start: int, end: int) -> List[int]:
    """
    Convert a range of blocks to an array of blocks (i.e., continuous).

    Sample input:
    start = 2
    end = 4

    Sample output:
    [2, 3, 4]
    """
    return list(range(start, end + 1))

def generate_graph(memberAvails: List[MemberAvail], slots: List[Slot]) -> nx.Graph:
    """
    Create a NetworkX graph to represent the member availabilities and the slot availabilities.
    """
    G = nx.Graph()
    G.add_node("source")
    G.add_node("sink")

    for s in slots:
        G.add_node(str(s.slotId))
        G.add_edge(str(s.slotId), "sink", capacity=s.numMembers)

    for member in memberAvails:
        G.add_node(member.email)
        G.add_edge("source", member.email, capacity=member.max_blocks)
        for member_slot in member.avail_slots:
            G.add_edge(member.email, str(member_slot.slot_id), capacity=1, weight=member_slot.prefer_level)

    return G


def mapping_to_results(mapping: dict, members: List[MemberSlot]):
    final_result = []
    for mem in members:
        if mem.email in mapping:
            slot_info = mapping[mem.email]
            # print(f"For {mem.email} the slot_info is {slot_info}")
            for slot_id in slot_info:
                if slot_info[slot_id] == 1:
                    final_result.append({"email": mem.email, "slot_id": slot_id})
                    # print(f"found mapping for email {mem.email} slot_id {slot_id}")
            # for slot in mapping[mem.email]:
            #     final_result.append({
            #         "email": mem.email,
            #         "slot_id": slot
            #     })
    print(final_result)
    return final_result
    # print(mapping)



def main():
    memberAvails = [
        MemberAvail("Ali", [MemberSlot("Ali", 1, 1), MemberSlot("Ali", 2, 2), MemberSlot("Ali", 3, 3)], 2),
        MemberAvail("Azi", [MemberSlot("Azi", 1, 3), MemberSlot("Azi", 2, 1), MemberSlot("Azi", 3, 1)], 2),
        MemberAvail("Ari", [MemberSlot("Ari", 1, 1), MemberSlot("Ari", 2, 1)], 1)
    ]
    slots = [
        Slot('{"name": "L1A", "slotId": 1, "numMembers": 2, "startBlock": 1, "endBlock": 3}'),
        Slot('{"name": "L2A", "slotId": 2, "numMembers": 2, "startBlock": 2, "endBlock": 4}'),
        Slot('{"name": "L3A", "slotId": 3, "numMembers": 1, "startBlock": 3, "endBlock": 5}')
    ]
    graph = generate_graph(memberAvails, slots)
    # print(graph)
    result = nx.max_flow_min_cost(graph, "source", "sink")
    mapping_to_results(result, memberAvails)

main()
