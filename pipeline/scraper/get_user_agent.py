import os
import random

USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agent.txt')
USER_AGENTS = []


def get_random_agent():
    with open(USER_AGENTS_FILE, "rb") as f:
        for line in f.readlines():
            if line:
                USER_AGENTS.append(line.strip()[1:-1])
    random.shuffle(USER_AGENTS)
    return random.choice(USER_AGENTS)


class RandomUserAgent(object):

    def __init__(self):
        self.USER_AGENT = []
        with open(USER_AGENTS_FILE, "rb") as f:
            for line in f.readlines():
                if line:
                    self.USER_AGENT.append(line.strip()[1:-1])
        random.shuffle(self.USER_AGENT)

    def get_user_agent(self):
        return random.choice(self.USER_AGENT)


random_user_agent = RandomUserAgent()
