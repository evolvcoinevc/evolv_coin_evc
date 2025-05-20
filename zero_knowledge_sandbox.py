
import hashlib
import random

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

class ZeroKnowledgeProver:
    def __init__(self, secret: str):
        self.secret = secret
        self.commitment = sha256(secret)

    def get_commitment(self):
        return self.commitment

    def respond_to_challenge(self, challenge: int):
        if challenge == 0:
            return self.commitment
        elif challenge == 1:
            return self.secret
        else:
            raise ValueError("Invalid challenge")

class ZeroKnowledgeVerifier:
    def __init__(self, expected_commitment: str):
        self.expected_commitment = expected_commitment

    def send_challenge(self):
        return random.choice([0, 1])

    def verify_response(self, challenge: int, response: str):
        if challenge == 0:
            return response == self.expected_commitment
        elif challenge == 1:
            return sha256(response) == self.expected_commitment
        else:
            return False

def simulate_zero_knowledge_proof():
    secret = "123456"
    prover = ZeroKnowledgeProver(secret)
    verifier = ZeroKnowledgeVerifier(prover.get_commitment())

    print("Starting Zero-Knowledge Proof Simulation")
    for round in range(5):
        print(f"\nRound {round + 1}:")
        challenge = verifier.send_challenge()
        print(f"Verifier sends challenge: {challenge}")
        response = prover.respond_to_challenge(challenge)
        print(f"Prover responds with: {response}")
        if verifier.verify_response(challenge, response):
            print("Verifier accepts the response ✅")
        else:
            print("Verifier rejects the response ❌")

simulate_zero_knowledge_proof()
