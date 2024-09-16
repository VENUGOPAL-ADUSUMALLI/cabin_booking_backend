from typing import List
from cabin_booking.databases.dtos import FloorWiseCabinDetailsDTO, CabinDetailsDTO
from cabin_booking.exception import SomethingWentWrongException
from cabin_booking.models import Cabin


class CabinDB:
    @staticmethod
    def get_cabins_details() -> List[FloorWiseCabinDetailsDTO]:
        try:
            cabins = Cabin.objects.all().select_related("floor").order_by("floor__order")
            floor_wise_cabin_details = {}
            for each_details in cabins:
                floor_name = each_details.floor.name
                if floor_name not in floor_wise_cabin_details:
                    floor_wise_cabin_details[floor_name] = FloorWiseCabinDetailsDTO(
                        floor=each_details.floor.name,
                        cabin=[]
                    )
                cabin_dict = CabinDetailsDTO(
                    cabin_id=str(each_details.id),
                    name=each_details.name,
                    cabin_type=each_details.type,
                    description=each_details.description
                )
                floor_wise_cabin_details[floor_name].cabin.append(cabin_dict)
            return list(floor_wise_cabin_details.values())
        except Exception:
            raise  SomethingWentWrongException()
