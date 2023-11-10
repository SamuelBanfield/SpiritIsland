from spirit_island.phases.phases_base import Phase

def run_phase(phase: Phase):
    phase.begin_phase()
    phase.update()