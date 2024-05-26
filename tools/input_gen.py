from operator import le
import random
import string

def my_print(*args):
    numbers = list(range(0, 10))
    weights = [4**x for x in numbers]
    weights.reverse()
    for arg in args:
        print(' ' * random.choices(numbers, weights, k=1)[0], end='')
        print(arg, end='')

def generate_atom(ids_set, depth=1):
    if depth > 1 and random.randint(0, 2) == 0:
        my_print('(')
        generate_xor(ids_set, depth - 1)
        my_print(')')
    else:
        letter = random.choice(list(ids_set))
        my_print(letter)
    pass

def generate_not(ids_set, depth=1):
    choices = list(range(0, 10))
    weights = [4**x for x in choices]
    weights.reverse()
    for _ in range(random.choices(choices, weights, k=1)[0]):
        my_print('!')
    generate_atom(ids_set, depth)

def generate_and(ids_set, depth=1):
    generate_not(ids_set, depth)
    numbers = list(range(0, 10))
    weights = [4**x for x in numbers]
    weights.reverse()
    for _ in range(random.choices(numbers, weights, k=1)[0]):
        my_print('+')
        generate_not(ids_set, depth)

def generate_or(ids_set, depth=1):
    generate_and(ids_set, depth)
    numbers = list(range(0, 10))
    weights = [4**x for x in numbers]
    weights.reverse()
    for _ in range(random.choices(numbers, weights, k=1)[0]):
        my_print('|')
        generate_and(ids_set, depth)

def generate_xor(ids_set, depth=1):
    generate_or(ids_set, depth)
    numbers = list(range(0, 10))
    weights = [4**x for x in numbers]
    weights.reverse()
    for _ in range(random.choices(numbers, weights, k=1)[0]):
        my_print('^')
        generate_or(ids_set, depth)

def generate_statement(ids_set, depth=1):
    generate_xor(ids_set, depth)
    my_print(random.choices(['=>', '<=>'], [3, 1], k=1)[0])
    generate_xor(ids_set, depth)

def generate_statements(ids_set, statements, min_statements, max_statements, depth=1):
    generate_statement(ids_set, depth)
    for i in range(statements if statements is not None else random.randint(min_statements, max_statements)):
        generate_nl(1, 4)
        generate_statement(ids_set, depth)


def generate_facts(ids_set, facts, min_facts, max_facts):
    ids_set = ids_set.copy()
    my_print('=')
    for _ in range(facts if facts is not None else random.randint(min_facts, max_facts)):
        letter = random.choice(list(ids_set))
        ids_set.remove(letter)
        my_print(letter)
    return ids_set

def generate_goals(ids_set, goals, min_goals, max_goals):
    ids_set = ids_set.copy()
    my_print('?')
    for _ in range(goals if goals is not None else random.randint(min_goals, max_goals)):
        letter = random.choice(list(ids_set))
        ids_set.remove(letter)
        my_print(letter)

def generate_comment():
    my_print('#')
    length = random.randint(0, 50)
    characters = string.ascii_letters + '     '
    my_print(''.join(random.choice(characters) for _ in range(length)))


def generate_ids_set(letters, min_letters, max_letters):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ids_set = set()
    for i in range(letters if letters is not None else random.randint(min_letters, max_letters)):
        ids_set.add(chars[i])
    return ids_set

def generate_char_random_times(c, min_size, max_size):
    numbers = list(range(min_size, max_size - 1))
    weights = [4**x for x in numbers]
    weights.reverse()
    my_print(c * random.choices(numbers, weights, k=1)[0])

def generate_nl(min_size, max_size):
    if random.randint(0, 5) == 0:
        generate_comment()
    generate_char_random_times('\n', min_size, max_size)

def generate_input(
        letters=None,
        min_letters=3,
        max_letters=10,
        statements=None,
        min_statements=5,
        max_statements=25,
        facts=None,
        min_facts=1,
        max_facts=5,
        goals=None,
        min_goals=1,
        max_goals=5,
        depth=3,
):
    if letters is not None:
        letters = max(1, min(letters, 26))
    max_letters = min(max_letters, 26)
    min_letters = max(1, min_letters)
    ids_set = generate_ids_set(letters, min_letters, max_letters)


    if statements is not None:
        statements = max(1, statements)
    min_statements = max(1, min_statements)
    max_statements = max(min_statements, max_statements)

    generate_nl(0, 5)
    generate_statements(ids_set, statements, min_statements, max_statements, depth)
    generate_nl(1, 5)


    if facts is not None:
        facts = max(0, min(facts, len(ids_set)))
    max_facts = min(max_facts, len(ids_set))
    min_facts = max(0, min_facts)

    facts_set = generate_facts(ids_set, facts, min_facts, max_facts)
    generate_nl(1, 5)


    goals_set = ids_set.difference(facts_set)
    if goals is not None:
        goals = max(1, min(goals, len(goals_set)))
    max_goals = min(max_goals, len(goals_set))
    min_goals = max(1, min_goals)
    generate_goals(goals_set, goals, min_goals, max_goals)
    generate_nl(0, 5)

def main():
    generate_input(
        # letters=6,
        min_letters=3,
        max_letters=10,
        # statements=5,
        min_statements=5,
        max_statements=25,
        # facts=2,
        min_facts=2,
        max_facts=4,
        # goals=2,
        min_goals=1,
        max_goals=3,
        depth=5,
    )

if __name__ == "__main__":
    main()