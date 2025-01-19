from typing import List
import networkx as nx
import json as json

class UserAvail:
    def __init__(self, email: str, available_blocks: List[int], prefer_not_blocks: List[int], max_blocks: int):
        self.email = "munce@ubc.ca"
        self.available_blocks = [1, 4, 5]
        self.prefer_not_blocks = [2, 3]
        self.max_blocks = 2

        self.email = email
        self.available_blocks = available_blocks
        self.prefer_not_blocks = prefer_not_blocks
        self.max_blocks = max_blocks

class Slot:
    def __init__(self, name: str, slotId: int, numMembers: int, startBlock: int, endBlock: int):
        self.name = "L2A"
        self.slotId = 2
        self.numMembers = 3
        self.startBlock = 2
        self.endBlock = 4

        self.name = name
        self.slotId = slotId
        self.numMembers = numMembers
        self.startBlock = startBlock
        self.endBlock = endBlock

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



def match_avails_to_slots(avails: List[UserAvail], slots: List[Slot]) -> List[MemberAvail]:
    """
    Change a block array to available slots.

    Sample input:
    [
        {
            "email": "munce@ubc.ca",
            "available_blocks": [1, 4, 5],
            "prefer_not_blocks": [2, 3],
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
    result = []
    for user in avails:
        user_concat_blocks = (user.available_blocks + user.prefer_not_blocks)
        user_concat_blocks.sort()
        member_avails_for_user = []
        for s in slots:
            arr = blocks_to_array(s.startBlock, s.endBlock)

            if is_subarray(arr, user_concat_blocks):
                score = 0
                # sum of available blocks + prefer not blocks is the "weight"
                for block in arr:
                    if block in user.available_blocks:
                        score += 1
                    elif block in user.prefer_not_blocks:
                        score += 2

                member_avails_for_user += [MemberSlot(user.email, s.slotId, score)]
        result_member_avail = MemberAvail(user.email, member_avails_for_user, user.max_blocks)
        result += [result_member_avail]
    return result

def is_subarray(subarray: List[int], array: List[int]) -> bool:
    sub_len = len(subarray)
    for i in range(len(array) - sub_len + 1):
        if array[i:i + sub_len] == subarray:
            return True
    return False


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
    # print(final_result)
    return final_result
    # print(mapping)



# def main():
#     # TODO delete this function
#     # memberAvails = [
#     #     MemberAvail("Ali", [MemberSlot("Ali", 1, 1), MemberSlot("Ali", 2, 2), MemberSlot("Ali", 3, 3)], 2),
#     #     MemberAvail("Azi", [MemberSlot("Azi", 1, 3), MemberSlot("Azi", 2, 1), MemberSlot("Azi", 3, 1)], 2),
#     #     MemberAvail("Ari", [MemberSlot("Ari", 1, 1), MemberSlot("Ari", 2, 1)], 1)
#     # ]
#     # slots = [
#     #     Slot('{"name": "L1A", "slotId": 1, "numMembers": 2, "startBlock": 1, "endBlock": 3}'),
#     #     Slot('{"name": "L2A", "slotId": 2, "numMembers": 2, "startBlock": 2, "endBlock": 4}'),
#     #     Slot('{"name": "L3A", "slotId": 3, "numMembers": 1, "startBlock": 3, "endBlock": 5}')
#     # ]
#     # graph = generate_graph(memberAvails, slots)
#     # # print(graph)
#     # result = nx.max_flow_min_cost(graph, "source", "sink")
#     # mapping_to_results(result, memberAvails)
#     # useravails = [
#     #     UserAvail('{"email": "munce@ubc.ca", "available_blocks": [1, 4, 5], "prefer_not_blocks": [2, 3], "max_blocks": 2}'),
#     #     UserAvail('{"email": "test@ubc.ca", "available_blocks": [1, 4, 5], "prefer_not_blocks": [], "max_blocks": 1}')
#     # ]

#     # slots = [
#     #     Slot('{"name": "L2A", "slotId": 2, "numMembers": 3, "startBlock": 2, "endBlock": 4}')
#     # ]

#     useravails_sample = [
#         UserAvail('{"email": "Ali", "available_blocks": [1, 2, 3, 4, 5], "prefer_not_blocks": [6, 7, 8, 9], "max_blocks": 2}'),
#         UserAvail('{"email": "Azi", "available_blocks": [4, 5, 6, 7, 8, 9], "prefer_not_blocks": [1, 2, 3], "max_blocks": 2}'),
#         UserAvail('{"email": "Ari", "available_blocks": [1, 2, 3, 4, 5, 6], "prefer_not_blocks": [], "max_blocks": 1}'),
#     ]

#     slots_sample = [
#         Slot('{"name": "L1A", "slotId": 1, "numMembers": 2, "startBlock": 1, "endBlock": 3}'),
#         Slot('{"name": "L2A", "slotId": 2, "numMembers": 2, "startBlock": 4, "endBlock": 6}'),
#         Slot('{"name": "L3A", "slotId": 3, "numMembers": 1, "startBlock": 7, "endBlock": 9}')
#     ]



#     result = match_avails_to_slots(useravails_sample, slots_sample)
#     [print(f"email is {user.email} available slots are {[f"id = {s.slot_id}; pref = {s.prefer_level}" for s in user.avail_slots]}") for user in result]
#     graph = generate_graph(result, slots_sample)
#     # print(graph)
#     result = nx.max_flow_min_cost(graph, "source", "sink")
#     mapping_to_results(result, useravails_sample)

# main()
