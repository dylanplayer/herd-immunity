
class Person:
    def __init__(self, id, is_infected, is_vaccinated):
        self.id = id
        self.is_infected = is_infected
        self.is_vaccinated = is_vaccinated
        self.is_dead = False

    def vaccinate(self):
        self.is_vaccinated = True

    def infect(self):
        self.is_infected = True