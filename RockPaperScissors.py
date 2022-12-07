import random

def play():
    user = input("Whats your choice?'r' for rock, 'p' for paper, 's' for scissors")
    print(user)
    computer = random.choice(['r', 'p', 's'])

    if user == computer:
        return "It's a Tie!"

    # r > s, s > p, p > r
    if is_win(user, computer):
        return "You Won!"

    return "You Lost!"

def is_win(user, computer):
    #return true if user wins
    if (user == "r" and computer == "s") or (user == "s" and computer == "p")\
        or (user == "p" and computer =="r"):
        return True

print(play())