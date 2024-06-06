import json
from datetime import datetime


class VahePealne:
    def __init__(self):
        self.content = []

    def read_file_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.content.clear()
        for row in data:
            self.content.append(FileContent(row["nimi"], row["sundinud"], row["amet"], row["surnud"]))

    def get_age(self, birthdate, deathdate=None):
        if deathdate is None:
            deathdate = datetime.now()
        age_years = deathdate.year - birthdate.year
        age_days = (deathdate - birthdate.replace(year=deathdate.year)).days
        if age_days < 0:
            age_years -= 1
            age_days = (deathdate - birthdate.replace(year=deathdate.year - 1)).days
        return age_years, age_days

    def get_statistics(self):
        now = datetime.now()
        total_people = 0
        longest_name = ""
        longest_name_length = 0
        oldest_alive = None
        oldest_alive_age_years = 0
        oldest_alive_age_days = 0
        oldest_dead = None
        oldest_dead_age_days = 0
        actors_count = 0
        born_1997_count = 0
        occupations = set()
        names_with_more_than_two_parts = 0
        same_birth_death_day_count = 0
        alive_count = 0
        dead_count = 0

        for person in self.content:
            total_people += 1

            if len(person.nimi) > longest_name_length:
                longest_name = person.nimi
                longest_name_length = len(person.nimi)

            occupations.add(person.amet)

            if person.sundinud.year == 1997:
                born_1997_count += 1

            if len(person.nimi.split()) > 2:
                names_with_more_than_two_parts += 1

            if "näitleja" in person.amet:
                actors_count += 1

            if person.surnud is None:
                alive_count += 1
                age_years, age_days = self.get_age(person.sundinud)
                if (age_years > oldest_alive_age_years) or (
                        age_years == oldest_alive_age_years and age_days > oldest_alive_age_days):
                    oldest_alive = person
                    oldest_alive_age_years = age_years
                    oldest_alive_age_days = age_days
            else:
                dead_count += 1

                if person.sundinud.strftime("%m-%d") == person.surnud.strftime("%m-%d"):
                    same_birth_death_day_count += 1

                age_days = (person.surnud - person.sundinud).days
                if age_days > oldest_dead_age_days:
                    oldest_dead = person
                    oldest_dead_age_days = age_days

        oldest_dead_age_years = oldest_dead_age_days // 365

        stats = {
            "1. Isikute arv kokku": total_people,
            "2. Kõige pikema nimi ja tähemärkide arv": f"{longest_name} ({longest_name_length})",
            "3. Kõige vanem elav inimene": f"{oldest_alive.nimi} ({oldest_alive_age_years} aastat, sündinud {oldest_alive.sundinud.strftime('%d.%m.%Y')})",
            "4. Kõige vanem surnud inimene": f"{oldest_dead.nimi} ({oldest_dead_age_years} aastat, sündinud {oldest_dead.sundinud.strftime('%d.%m.%Y')}, surnud {oldest_dead.surnud.strftime('%d.%m.%Y')})",
            "5. Näitlejate koguarv": actors_count,
            "6. Sündinud 1997 aastal": born_1997_count,
            "7. Kui palju on erinevaid elukutseid": len(occupations),
            "8. Nimi sisaldab rohkem kui kaks nime": names_with_more_than_two_parts,
            "9. Sünniaeg ja surmaaeg sama kuupäev v.a. aasta": same_birth_death_day_count,
            "10. Elavaid ja surnud isikud": f"{alive_count} + {dead_count}"
        }

        return stats


class FileContent:
    def __init__(self, nimi, sundinud, amet, surnud):
        self.nimi = nimi
        self.sundinud = datetime.strptime(sundinud, "%Y-%m-%d")
        self.amet = amet
        if surnud != "0000-00-00":
            self.surnud = datetime.strptime(surnud, "%Y-%m-%d")
        else:
            self.surnud = None
