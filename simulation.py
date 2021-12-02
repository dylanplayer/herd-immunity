import sys
import math
import random

from virus import Virus
from person import Person
from logger import Logger

class Simulation:
    def __init__(self, init_population_size, percent_init_vaccinated, virus_name, mortality_rate, reproduction_rate, initally_infected):
        self.init_population_size = init_population_size
        self.total_person_objects = 0
        self.virus = Virus(virus_name, mortality_rate, reproduction_rate)
        self.vulnerable_population = self.create_vulnerable_population(init_population_size, percent_init_vaccinated, initally_infected)
        self.vaccinated_population = self.create_vaccinated_population(init_population_size, percent_init_vaccinated)
        self.infected_population = self.create_infected_population(initally_infected)
        self.dead_population = []
        self.fileName = f"{virus_name}_simulation_pop_{init_population_size}_vp_{percent_init_vaccinated}_infected_{initally_infected}.txt"
        self.logger = Logger(self.fileName)
        self.logger.write_metadata(init_population_size, percent_init_vaccinated, virus_name, mortality_rate, reproduction_rate)
        # print('init-' ,f'Vulnerable: {len(self.vulnerable_population)}', f'Vaccinated: {len(self.vaccinated_population)}', f'Infected: {len(self.infected_population)}', f'Dead: {len(self.dead_population)}')
        self.run()

    def create_vaccinated_population(self, population_size, percent_init_vaccinated):
        population = []
        for i in range(math.floor(population_size * percent_init_vaccinated)):
            population.append(Person(self.total_person_objects, False, True))
            self.total_person_objects += 1
        return population

    def create_vulnerable_population(self, population_size, percent_init_vaccinated, initally_infected):
        population = []
        for i in range(population_size - math.floor(population_size * percent_init_vaccinated) - initally_infected):
            population.append(Person(self.total_person_objects, False, False))
            self.total_person_objects += 1
        return population

    def create_infected_population(self, initally_infected):
        population = []
        for i in range(initally_infected):
            population.append(Person(self.total_person_objects, True, True))
            self.total_person_objects += 1
        return population

    def simulation_is_not_over(self):
        if len(self.vulnerable_population) == 0 or len(self.infected_population) == 0:
            return False
        else:
            return True

    def interact(self, infected_person, uninfected_person):
        self.interactions += 1
        if not uninfected_person.is_vaccinated:
            if self.virus.reproduction_rate >= random.random():
                uninfected_person.infect()
                self.newly_infected.append(uninfected_person)
                for person in self.vulnerable_population:
                    if person.id == uninfected_person.id:
                        self.vulnerable_population.remove(uninfected_person)
                        break                        

    def check_infection_survival(self):
        for person in self.infected_population:
            if self.virus.mortality_rate >= random.random():
                self.new_deaths += 1
                self.dead_population.append(person)
            else:
                self.vaccinated_population.append(person)
            self.infected_population.remove(person)

    def step(self):
        self.current_step += 1
        self.newly_infected = []
        self.interactions = 0
        self.new_deaths = 0
        uninfected_population = self.vaccinated_population + self.vulnerable_population
        for person in self.infected_population:
            for i in range(100):
                self.interact(person, random.choice(uninfected_population))
        self.check_infection_survival()
        self.infected_population + self.newly_infected.copy()
        
    def run(self):
        self.current_step = 0
        while self.simulation_is_not_over():
            self.step()
            self.logger.log_time_step(self.current_step, self.interactions, len(self.infected_population), self.new_deaths, len(self.vaccinated_population), len(self.vulnerable_population))
            # print(f'{self.current_step}. |' ,f'Interactions: {self.interactions},',f'Vulnerable: {len(self.vulnerable_population)},', f'Vaccinated: {len(self.vaccinated_population)},', f'New Infections: {len(self.infected_population)},', f'Dead: {len(self.dead_population)}')

if __name__ == "__main__":
    params = sys.argv[1:]

    population_size = int(params[0])
    percent_vaccinated = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    reproduction_rate = float(params[4])
    initally_infected = int(params[5])

    sim = Simulation(population_size, percent_vaccinated, virus_name, mortality_rate, reproduction_rate, initally_infected)