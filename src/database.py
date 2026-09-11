# basic imports

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import func
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import cast, Any

# Base class creation

class _Base(DeclarativeBase):
    pass

# Database table classes

class _BatteryPercent(_Base):
    __tablename__ = "batteriespercent"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    value = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

class _BatteryType(_Base):
    __tablename__ = "batteriestypes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    value = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

class _LQI(_Base):
    __tablename__ = "deviceslqi"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    value = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

class _RSSI(_Base):
    __tablename__ = "devicesrssi"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    value = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

# Data classes for usage in the whole application! not only here

@dataclass
class _BatteryPercentClass:
    name: str
    entity_id: str
    value: str
    date: datetime | None

@dataclass
class _BatteryTypeClass:
    name: str
    entity_id: str
    value: str
    date: datetime | None

@dataclass
class _LQIClass:
    name: str
    entity_id: str
    value: str
    date: datetime | None

@dataclass
class _RSSIClass:
    name: str
    entity_id: str
    value: str
    date: datetime | None

# Defining class which instance is going to be used in other code scripts

class HADBData:
    def __init__(self):
        # taking path to program directory
        baseDir = Path(__file__).resolve().parent
        # creating path to "data" folder and making it (if does not exist)
        dbDir = baseDir / "data"
        dbDir.mkdir(parents = True, exist_ok = True)
        # final path to db file
        dbPath = dbDir / "hadbdata.db"
        # initialising db engine
        self.engine = create_engine(f"sqlite:///{dbPath}")
        # create hadbdata.db if not exist
        _Base.metadata.create_all(self.engine)

    def _get_session(self):
        return Session(self.engine)

    # methods for classical data saving

    def addBatteryPercentEntry(
            self,
            entry: _BatteryPercentClass
    ) -> None:
        if entry.date is None:
            entry.date = datetime.now()

        with self._get_session() as session:
            battery = _BatteryPercent(
            name = entry.name,
            entity_id = entry.entity_id,
            value = entry.value,
            date = entry.date
        )
            session.add(battery)
            session.commit()

    def addBatteryPercentEntries(
            self,
            entries : list[_BatteryPercentClass]
    ) -> None:
        for entry in entries:
            self.addBatteryPercentEntry(entry)

    def addBatteryTypeEntry(
            self,
            entry: _BatteryTypeClass
    ) -> None:
        if entry.date is None:
            entry.date = datetime.now()

        with self._get_session() as session:
            battery = _BatteryType(
            name = entry.name,
            entity_id = entry.entity_id,
            value = entry.value,
            date = entry.date
        )
            session.add(battery)
            session.commit()

    def addBatteryTypeEntries(
            self,
            entries : list[_BatteryTypeClass]
    ) -> None:
        for entry in entries:
            self.addBatteryTypeEntry(
                entry
            )

    def addLQIEntry(
            self,
            entry: _LQIClass
    ) -> None:
        if entry.date is None:
            entry.date = datetime.now()
        with self._get_session() as session:
            lqi = _LQI(
                name = entry.name,
                entity_id = entry.entity_id,
                value = entry.value,
                date = entry.date
            )
            session.add(lqi)
            session.commit()

    def addLQIEntries(self, entities: list[_LQIClass]) -> None:
        for entry in entities:
            self.addLQIEntry(
                entry
            )

    def addRSSIEntry(
            self,
            entry: _RSSIClass
    ) -> None:
        if entry.date is None:
            entry.date = datetime.now()

        with self._get_session() as session:
            rssi = _RSSI(
                name = entry.name,
                entity_id = entry.entity_id,
                value = entry.value,
                date = entry.date
            )
            session.add(rssi)
            session.commit()

    def addRSSIEntries(self, entries: list[_RSSIClass]) -> None:
        for entry in entries:
            self.addRSSIEntry(
                entry
            )

    # methods for loading data specially for Ollama

    def getAllBatteryTypeEntries(self) -> list[_BatteryTypeClass]:
        entries : list[_BatteryTypeClass] = []
        with self._get_session() as session:
            rows = session.query(_BatteryType).all()
            for row in rows:
                entry = _BatteryTypeClass(
                    name = str(row.name),
                    entity_id = str(row.entity_id),
                    value = str(row.value),
                    date = cast(datetime | None, cast(Any, row.date))
                )
                entries.append(entry)
        return entries

    def getAllBatteryPercentEntries(self) -> list[_BatteryPercentClass]:
        entries : list[_BatteryPercentClass] = []
        with self._get_session() as session:
            rows = session.query(_BatteryPercent).all()
            for row in rows:
                entry = _BatteryPercentClass(
                    name = str(row.name),
                    entity_id = str(row.entity_id),
                    value = str(row.value),
                    date = cast(datetime | None, cast(Any, row.date))
                )
                entries.append(entry)
        return entries

    def getAllLQIEntries(self) -> list[_LQIClass]:
        entries : list[_LQIClass] = []
        with self._get_session() as session:
            rows = session.query(_LQI).all()
            for row in rows:
                entry = _LQIClass(
                    name = str(row.name),
                    entity_id = str(row.entity_id),
                    value = str(row.value),
                    date = cast(datetime | None, cast(Any, row.date))
                )
                entries.append(entry)
        return entries

    def getAllRSSIEntries(self) -> list[_RSSIClass]:
        entries : list[_RSSIClass] = []
        with self._get_session() as session:
            rows = session.query(_RSSI).all()
            for row in rows:
                entry = _RSSIClass(
                    name = str(row.name),
                    entity_id = str(row.entity_id),
                    value = str(row.value),
                    date = cast(datetime | None, cast(Any, row.date))
                )
                entries.append(entry)
        return entries

# methods for loading latest data per entity

    def getLatestBatteryTypeEntries(self) -> list[_BatteryTypeClass]:
        entries : list[_BatteryTypeClass] = []
        with self._get_session() as session:
            subq = (
                session.query(
                    _BatteryType.entity_id,
                    func.max(_BatteryType.date).label("max_date")
                )
                .group_by(_BatteryType.entity_id)
                .subquery()
            )
            rows = (
                session.query(_BatteryType)
                .join(
                    subq,
                    (_BatteryType.entity_id == subq.c.entity_id)
                    & (_BatteryType.date == subq.c.max_date)
                )
                .all()
            )
            for row in rows:
                entry = _BatteryTypeClass(
                    name = str(row.name),
                    entity_id = str(row.entity_id),
                    value = str(row.value),
                    date = cast(datetime | None, cast(Any, row.date))
                )
                entries.append(entry)
        return entries

    def getLatestBatteryPercentEntries(self) -> list[_BatteryPercentClass]:
        entries : list[_BatteryPercentClass] = []
        with self._get_session() as session:
            subq = (
                session.query(
                    _BatteryPercent.entity_id,
                    func.max(_BatteryPercent.date).label("max_date")
                )
                .group_by(_BatteryPercent.entity_id)
                .subquery()
            )
            rows = (
                session.query(_BatteryPercent)
                .join(
                    subq,
                    (_BatteryPercent.entity_id == subq.c.entity_id)
                    & (_BatteryPercent.date == subq.c.max_date)
                )
                .all()
            )
            for row in rows:
                entry = _BatteryPercentClass(
                    name = str(row.name),
                    entity_id = str(row.entity_id),
                    value = str(row.value),
                    date = cast(datetime | None, cast(Any, row.date))
                )
                entries.append(entry)
        return entries

    def getLatestLQIEntries(self) -> list[_LQIClass]:
        entries : list[_LQIClass] = []
        with self._get_session() as session:
            subq = (
                session.query(
                    _LQI.entity_id,
                    func.max(_LQI.date).label("max_date")
                )
                .group_by(_LQI.entity_id)
                .subquery()
            )
            rows = (
                session.query(_LQI)
                .join(
                    subq,
                    (_LQI.entity_id == subq.c.entity_id)
                    & (_LQI.date == subq.c.max_date)
                )
                .all()
            )
            for row in rows:
                entry = _LQIClass(
                    name = str(row.name),
                    entity_id = str(row.entity_id),
                    value = str(row.value),
                    date = cast(datetime | None, cast(Any, row.date))
                )
                entries.append(entry)
        return entries

    def getLatestRSSIEntries(self) -> list[_RSSIClass]:
        entries : list[_RSSIClass] = []
        with self._get_session() as session:
            subq = (
                session.query(
                    _RSSI.entity_id,
                    func.max(_RSSI.date).label("max_date")
                )
                .group_by(_RSSI.entity_id)
                .subquery()
            )
            rows = (
                session.query(_RSSI)
                .join(
                    subq,
                    (_RSSI.entity_id == subq.c.entity_id)
                    & (_RSSI.date == subq.c.max_date)
                )
                .all()
            )
            for row in rows:
                entry = _RSSIClass(
                    name = str(row.name),
                    entity_id = str(row.entity_id),
                    value = str(row.value),
                    date = cast(datetime | None, cast(Any, row.date))
                )
                entries.append(entry)
        return entries