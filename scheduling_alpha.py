import itertools
import datetime
import pprint

class Schedule:

    def __init__(self, t, str):
        self.times = {
            'm': t if str.find('m') != -1 else (datetime.time(0,0), datetime.time(0,0)),
            't': t if str.find('t') != -1 else (datetime.time(0,0), datetime.time(0,0)),
            'w': t if str.find('w') != -1 else (datetime.time(0,0), datetime.time(0,0)),
            'th': t if str.find('Th') != -1 else (datetime.time(0,0), datetime.time(0,0)),
            'f': t if str.find('f') != -1 else (datetime.time(0,0), datetime.time(0,0)),
        }

    def __repr__(self):
        s = ''
        t = ''
        for (date, time) in self.times.items():
            if time != (datetime.time(0,0), datetime.time(0,0)):
                s += date
                t = str(time[0]) + ' - ' + str(time[1])
        s += t
        return s

    def compatible(self, other):
        for (t1, t2) in zip(self.times.values(), other.times.values()):
            if not ((t2[0] <= t2[1] <= t1[0]) or (t2[1] >= t2[0] >= t1[1])):
                return False
        return True

def schedule(courses, filters=[]):
    # All possible combinations of courses
    # TODO: Intelligent, filter-resistant combinations
    combos = list(itertools.product(*courses.values()))
    
    
    # Accumulates all non-conflicting schedules
    compatible = []
    for combination in combos:
        # Start the combinations off with the filters (excluded times)
        conflicts = filters.copy()
        works = True
        for el in combination:
            # For each course time assignment, make sure it is not conflicted
            if all(map(lambda x: el.compatible(x), conflicts)):
                # If it's not a conflict, add it to conflicts
                conflicts.append(el)
            else:
                # This schedule does not work
                works = False
                break
        if works:
            # If the schedule works, add it to the compatible courses
            compatible.append(combination)

    # Reconstruct compatible by pairing with course
    recon_compat = []
    for compat in compatible:
        # Tuple, match
        curr = {}
        for (course, time) in zip(courses.keys(), compat):
            curr[course] = time
        recon_compat.append(curr)

    return recon_compat

def t(sh, sm, eh, em):
    return (datetime.time(sh, sm), datetime.time(eh, em))



choices = {
    'CS3650': [Schedule(t(9,50,11,30), 'tf'), Schedule(t(15,25,17,5), 'tf'), Schedule(t(13,35,15,15), 'tf')],
    'CS3000': [Schedule(t(9,50,11,30), 'tf'), Schedule(t(15,25,17,5), 'tf'), Schedule(t(13,35,15,15), 'tf')],
    'CS3001': [Schedule(t(10,30,11,35), 'w'), Schedule(t(11,45,12,50), 'w'), Schedule(t(8,0,9,5), 'w'), Schedule(t(9,15,10,20), 'w'), Schedule(t(13,35,14,40), 'w')],
    'CY2550': [Schedule(t(9,50,11,30), 'tf'), Schedule(t(13,35,15,15), 'tf'), Schedule(t(14,50,16,30), 'mw')],
    'GAME2500': [Schedule(t(9,50,11,30), 'tf'), Schedule(t(14,50,16,30), 'mw'), Schedule(t(13,35,15,15), 'tf'), Schedule(t(11,45,13,25), 'mw'), Schedule(t(13,35,15,15), 'tf')],
}

potentials = schedule(choices, [Schedule(t(8,0,11,0), 'mtwThf')])
pprint.PrettyPrinter().pprint(potentials)