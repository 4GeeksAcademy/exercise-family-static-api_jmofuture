from typing import Dict, Any
from random import randint

class FamilyStructure:
    def __init__(self, last_name: str):
        self.last_name = last_name
        self._members = [
            {
                "id": self._generate_id(),
                "first_name": "John",
                "last_name": self.last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generate_id(),
                "first_name": "Jane",
                "last_name": self.last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": self._generate_id(),
                "first_name": "Jimmy",
                "last_name": self.last_name,
                "age": 5,
                "lucky_numbers": [1]
            }
        ]


    def _generate_id(self):
        return randint(0, 99999999)
    

    def add_member(self, member: Dict[str, Any]) -> Dict[str, Any]:
 
        if "id" not in member:
            member["id"] = self._generate_id()

        member["last_name"] = self.last_name

        if "first_name" not in member or "age" not in member or "lucky_numbers" not in member:
            raise ValueError("El miembro debe tener 'first_name', 'age' y 'lucky_numbers'.")

        self._members.append(member)
        
        return member


    def delete_member(self, member_id: int) -> bool:

        for i, member in enumerate(self._members):

            if member["id"] == member_id:
                del self._members[i]

                return True
            
        return False


    def get_member(self, id: int) -> Dict[str, Any]:

        for member in self._members:

            if member['id'] == id:

                return member
        return None


    def get_all_members(self) -> list:
        return self._members.copy()

if __name__ == "__main__":
    family = FamilyStructure("Jackson")

    print(family.get_all_members())
