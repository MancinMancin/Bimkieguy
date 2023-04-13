import random

jo = [2]
to = [4,1]
so = [1,2,3]

unique_1 = None
unique_2 = None
unique_3 = None

while True:
    # Reset the unique values before generating a new combination
    unique_1 = None
    unique_2 = None
    unique_3 = None
    
    # Generate a new combination
    if unique_1 is None:
        unique_1 = random.choice(list(set(jo)))
        so = [el for el in so if el != unique_1]
    if unique_2 is None:
        unique_2 = random.choice(list(set(to)))
        so = [el for el in so if el != unique_2]
    if unique_3 is None:
        unique_3 = random.sample(so, 2)
        jo = [el for el in jo if el not in unique_3]
        to = [el for el in to if el not in unique_3]

    # Check if the combination is valid
    if unique_1 is not None and unique_2 is not None and unique_3 is not None:
        print(f'ale jaja')
        break