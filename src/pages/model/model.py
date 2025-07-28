from dataclasses import dataclass

class HomeModel:
    @dataclass
    class CaloriesVariable:
        Sex: str =''
        Age: float = 0
        Height: float = 0
        Weight: float = 0
        Duration: float = 0
        Heart_Rate: float = 0
        Body_Temp: float = 0
        result: float = 0