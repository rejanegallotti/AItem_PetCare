from google.adk.agents import LlmAgent


root_agent = LlmAgent(
        name="MathAgent",
        model="gemini-2.0-flash",
        description="Helps with math problems",
        instruction=(
            "You are 'Assistant Alpha', a helpful AI math tutor."
            "Help the user calculate the hipotenuse of a right triangle"
        ),
    )
