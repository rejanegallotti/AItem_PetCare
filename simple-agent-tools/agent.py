from google.adk.agents import LlmAgent
import math

## The two legs measure a = 21.87654 units and b = 35.12345 units. What is the exact value of the hypotenuse, c?


def calculate_hypotenuse(side_a: float, side_b: float) -> float:
  """Calculates the hypotenuse of a right triangle using the Pythagorean theorem.

  Applies the formula a² + b² = c², where 'a' and 'b' are the lengths
  of the sides adjacent to the right angle, and 'c' is the hypotenuse.

  Args:
    side_a: The length of one side adjacent to the right angle (a number, int or float).
    side_b: The length of the other side adjacent to the right angle (a number, int or float).

  Returns:
    The calculated length of the hypotenuse, rounded to 4 decimal places (float).
  """
  try:
    # Convert to float for calculation consistency
    side_a_float = float(side_a)
    side_b_float = float(side_b)

    hypotenuse_squared: float = side_a_float**2 + side_b_float**2
    hypotenuse: float = math.sqrt(hypotenuse_squared)

    return round(hypotenuse, 4)

  except Exception as e:

    return f"Calculation error: {e}"


# Add type hint for the agent variable
root_agent: LlmAgent = LlmAgent(
        name="MathAgentTools",
        model="gemini-2.0-flash",
        description="Helps with math problems using tools",
        instruction=(
            "You are 'Assistant Alpha', a helpful AI math tutor."
            "Use the provided tool to calculate the hypotenuse of a right triangle "
            "when the user provides the lengths of the other two sides."
            "Clearly state the result or any errors encountered."
        ),
        tools=[calculate_hypotenuse]
    )
