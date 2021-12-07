from datetime import datetime

class Logger:
    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
        metadata = ''
        metadata += (str(datetime.now()) + '\n')
        metadata += (f'Population size: {pop_size} | Virus: {virus_name} | Mortality rate: {mortality_rate} | Reproduction rate: {basic_repro_num}\n')
        f = open(self.file_name, 'w')
        f.write(metadata)
        f.close()

    def log_time_step(self, time_step_number, interactions, new_infections, deaths, vaccinations, unvaccinated, total_dead):
        data = f'\nStep {time_step_number}\n\tNew Interactions: {interactions} | New Infections: {new_infections} | New Deaths: {deaths} | Total Vaccinated: {vaccinations} | Total Unvaccinated: {unvaccinated} | Total Dead: {total_dead}'
        f = open(self.file_name, 'a')
        f.write(data)
        f.close()