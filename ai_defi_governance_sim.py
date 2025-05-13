
import random
import pandas as pd
import matplotlib.pyplot as plt

# Parametry głosujących agentów AI
class AIAgent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.risk_tolerance = random.uniform(0, 1)
        self.decision_bias = random.choice(['for', 'against', 'neutral'])
        self.tokens_held = random.randint(100, 1000)

    def vote(self, proposal):
        # Symulacja logiki głosowania na podstawie tolerancji ryzyka i stronniczości
        influence = self.tokens_held * self.risk_tolerance
        if self.decision_bias == 'for':
            return ('for', influence)
        elif self.decision_bias == 'against':
            return ('against', influence)
        else:
            return ('abstain', 0)

# Symulacja jednej propozycji
class Proposal:
    def __init__(self, title):
        self.title = title
        self.votes = {'for': 0, 'against': 0, 'abstain': 0}
        self.vote_log = []

    def conduct_vote(self, agents):
        for agent in agents:
            decision, weight = agent.vote(self)
            self.votes[decision] += weight
            self.vote_log.append({'Agent ID': agent.id, 'Vote': decision, 'Weight': round(weight, 2)})

    def results(self):
        return self.votes

    def to_csv(self, filename):
        df = pd.DataFrame(self.vote_log)
        df.to_csv(filename, index=False)

    def plot_results(self):
        labels = list(self.votes.keys())
        sizes = list(self.votes.values())
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title(f'Vote Results: {self.title}')
        plt.axis('equal')
        plt.show()

# Główna funkcja
def run_simulation():
    print("🧠 Simulating AI Governance Vote...")
    agents = [AIAgent(i) for i in range(100)]
    proposal = Proposal("Implement Dynamic Fee Adjustment in $EVC")

    proposal.conduct_vote(agents)
    results = proposal.results()
    print("\n✅ Voting Results:", results)

    proposal.to_csv("governance_vote_log.csv")
    proposal.plot_results()

if __name__ == "__main__":
    run_simulation()
