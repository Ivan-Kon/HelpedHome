import sqlalchemy
from sqlalchemy import create_engine


class Tables:
    def __init__(self,
                 url: str = None,
                 area: str = None,
                 money: int | list[int] = None,
                 devices: list = None,
                 ) -> None:

        self.area = area
        self.money = money
        self.devices = devices if devices else []
        self.url = url
        self.devices_info = {}
        self.engine = create_engine('sqlite:///myDatabase.db', pool_pre_ping=True)
        self.metadata = sqlalchemy.MetaData()
        self.conn = self.engine.connect()

        # Создаем таблицу, если её нет
        self.flats = sqlalchemy.Table(
            "flats", self.metadata,
            sqlalchemy.Column("flat_id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("flat_url", sqlalchemy.Text),
            sqlalchemy.Column("flat_price", sqlalchemy.INTEGER),
            sqlalchemy.Column("flat_area", sqlalchemy.Text),
            sqlalchemy.Column("flat_fridge", sqlalchemy.BOOLEAN),
            sqlalchemy.Column("flat_tv", sqlalchemy.BOOLEAN),
            sqlalchemy.Column("flat_conditioner", sqlalchemy.BOOLEAN),
            sqlalchemy.Column("flat_washing_machine", sqlalchemy.BOOLEAN),
            sqlalchemy.Column("flat_dishwasher", sqlalchemy.BOOLEAN),
            sqlalchemy.Column("flat_wifi", sqlalchemy.BOOLEAN),
        )

        # Создаем таблицу в базе данных
        self.metadata.create_all(self.engine)

    def find_flats(self):
        result = self.conn.execute(self.flats.select())
        return result.fetchall()

    def add_flat(self):
        # Сначала заполняем devices_info
        self.return_devices()

        # Создаем словарь с данными
        values = {
            "flat_url": self.url,
            "flat_price": self.money,
            "flat_area": self.area,
            **self.devices_info  # Распаковываем словарь с устройствами
        }

        # Выполняем вставку один раз
        self.conn.execute(self.flats.insert().values(values))
        self.conn.commit()

    def return_devices(self):
        # Сначала устанавливаем все значения в False
        self.devices_info = {
            "flat_fridge": False,
            "flat_tv": False,
            "flat_conditioner": False,
            "flat_washing_machine": False,
            "flat_dishwasher": False,
            "flat_wifi": False,
        }

        # Затем устанавливаем True для тех устройств, которые есть в списке
        for device in self.devices:
            if device == "Холодильник":
                self.devices_info["flat_fridge"] = True
            elif device == "Телевизор":
                self.devices_info["flat_tv"] = True
            elif device == "Кондиционер":
                self.devices_info["flat_conditioner"] = True
            elif device == "Стиральная машина":
                self.devices_info["flat_washing_machine"] = True
            elif device == "Посудомоечная машина":
                self.devices_info["flat_dishwasher"] = True
            elif device == "Интернет":
                self.devices_info["flat_wifi"] = True
