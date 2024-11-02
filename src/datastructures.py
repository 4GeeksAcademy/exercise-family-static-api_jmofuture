
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name: str) -> None:
        self.last_name = last_name

        # example list of members
        self._members = []


    def _generateId(self) -> int:
        return randint(0, 99999999)


    def add_member(self, member: dict) -> None:

        member["id"] = self._generateId()
        member["last_name"] = self.last_name

        self._members.append(member)


    def delete_member(self, id: int) -> None:

        if not self._members:
            print("La lista está vacía.")
            return

        for member in self._members:
            if member['id'] == id:
                self._members.remove(member)  
                print(f"Se eliminó a {member['first_name']}")
                return
        
        print(f"No se encontró ningún miembro con ID {id}.")


    def get_member(self, id: int) -> None:

        if not self._members:
            print("La lista está vacía.")
            return

        for member in self._members:
            if member['id'] == id:
                print(f"Se eliminó a {member}")
                return
        
        print(f"No se encontró ningún miembro con ID {id}.")

    # this method is done, it returns a list with all the family members
    def get_all_members(self) -> None:
        return self._members
    
    

if __name__ == "__main__":

    family = FamilyStructure("Jackson")


    family.add_member({"first_name": "Jean", "age": 25, "lucky_numbers": [7, 14, 21]})
    family.add_member({"first_name": "Lucia", "age": 30, "lucky_numbers": [3, 5, 9]})


    print(family.get_all_members())

