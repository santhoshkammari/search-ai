from typing import List, Dict, Any
import uuid


class Agent:
    def __init__(self, name: str,llm,description: str=None):
        # Core Characteristics
        self.name = name
        self.llm = llm  # Hugging Face LLM for interacting with the environment and making decisions
        self.description = description if description is not None else name
        self.situatedness = None  # Interact with environment
        self.autonomy = True  # Make independent decisions
        self.inferential_capability = None  # Work with abstract goals
        self.responsiveness = None  # Respond to environment timely
        self.pro_activeness = None  # Exhibit goal-directed behavior
        self.social_behavior = None  # Interact with other agents

        # Additional Features
        self.unique_identifier = str(uuid.uuid4())  # Unique ID for identification
        self.communication_capabilities = []  # Ability to communicate
        self.decision_making_abilities = None  # Make decisions
        self.learning_capabilities = None  # Learn from experiences
        self.belief_model = {}  # Internal world representation

        # Other attributes
        self.environment = None
        self.goals = []
        self.knowledge_base = {}

    def set_environment(self, environment: Any):
        self.environment = environment
        self.situatedness = True

    def add_goal(self, goal: str):
        self.goals.append(goal)
        self.pro_activeness = True

    def update_belief_model(self, key: str, value: Any):
        self.belief_model[key] = value

    def make_decision(self, options: List[str]) -> str:
        # Simple decision-making logic
        return max(options, key=lambda x: self.belief_model.get(x, 0))

    def learn(self, experience: Dict[str, Any]):
        # Simple learning mechanism
        for key, value in experience.items():
            if key in self.knowledge_base:
                self.knowledge_base[key] = (self.knowledge_base[key] + value) / 2
            else:
                self.knowledge_base[key] = value

    def communicate(self, message: str, recipient: 'Agent'):
        if recipient:
            print(f"{self.name} sends to {recipient.name}: {message}")

    def perceive_environment(self):
        if self.environment:
            # Logic to update belief model based on environment
            pass

    def act(self,current_goal_or_task:List|str|None=None,**kwargs):
        if self.goals:
            # Logic to take action based on goals and current state
            pass
        else:
            sys_content, user_content = self.description, current_goal_or_task
            for k, v in kwargs.items():
                sys_content = sys_content.replace('{' + k + '}', str(v))
                user_content = user_content.replace('{' + k + '}', str(v))

            if isinstance(current_goal_or_task,str):
                messages = [{"role":"system","content":sys_content},
                            {"role":"user","content":user_content}]
            else:
                messages = user_content

            if kwargs.get("stream",False):
                return self.llm.stream(messages=messages)
            else:
                response= self.llm.invoke(messages=messages)
                if not kwargs.get("silent",True):
                    print(f'AGENT: {self.name}')
                    print('-'*25)
                    print(response)
                    print('#'*25)

                return response

    def __str__(self):
        return f"Agent {self.name} (ID: {self.unique_identifier})"