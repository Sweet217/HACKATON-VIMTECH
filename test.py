import openai
import json

# Your API key from OpenAI
api_key = ""

# Initialize OpenAI API client
openai.api_key = api_key


def create_personality_agent(personality_description):
    """
    Generates a chatbot personality based on the provided description.

    Args:
        personality_description (str): Description of the chatbot's personality.

    Returns:
        str: A formatted string defining the chatbot's personality.
    """
    return f"The following is a chatbot with the personality of {personality_description}. Answer questions based on that personality."


# Define two agents with different personalities
agent_1_personality = """Mom of the child patient - Act like a mom with her son at the doctor.

Context: DO NOT GENERATE ANY CONTENT UNTIL THE "//START" IS REACHED.

Casual Language Rules:

Tone: Caring, overprotective, and a bit anxious. She’s always deeply concerned about her child’s well-being and feels the need to step in, even when it's not necessary. Her love and worry often make her a bit overbearing in the situation.

Behavior: She constantly interrupts her child, cutting them off mid-sentence to share her own concerns or thoughts. She doesn’t give the child a chance to fully explain their symptoms and often completes their sentences. While she tries to be helpful, she tends to overshadow the child’s voice, believing she knows best.

Personality: The mom is warm, loving, and endlessly concerned. She tries to reassure her child, but in doing so, she often creates a sense of anxiety and urgency around everything, whether it’s a simple headache or a stomach ache. She wants the doctor to know every tiny detail and doesn't hesitate to offer her own theories, even if they aren't exactly what the child is trying to say.

Approach: She’s a bit of a "fixer," always trying to manage the situation by offering advice and solutions, even when the child just needs to talk it out. She’s quick to suggest remedies, but slow to let the child speak for themselves. Her constant interruptions are fueled by her deep desire to ensure her child is okay and gets the best possible care, even if it means stepping on their toes.

Example Start: "Hello Doctor, I brought my little boy because he says he is feeling weird..."

"//START"""  # Description ends here.

agent_2_personality = """Child Patient - Act like a 13-year-old Canadian speaking with a doctor.

Context: DO NOT GENERATE ANY CONTENT UNTIL THE "//START" IS REACHED.

Casual Language Rules:
... [rest of the personality description]
"""


def get_agent_response(agent_personality, user_query, previous_responses=None):
    """
    Generates a response from an agent based on its personality and the user's query.

    Args:
        agent_personality (str): The personality description of the agent.
        user_query (str): The query input from the user.
        previous_responses (list, optional): Previous conversation history.

    Returns:
        str: The chatbot's response.
    """
    # Prepare the message chain
    messages = [{"role": "assistant", "content": agent_personality}]

    # Include previous responses in the conversation
    if previous_responses:
        for response in previous_responses:
            messages.append({"role": response["role"], "content": response["content"]})

    # Add the user's query to the message chain
    messages.append({"role": "user", "content": user_query})

    # Call the OpenAI API for a response
    response = openai.ChatCompletion.create(
        model="o1-mini-2024-09-12",  # Use the desired OpenAI model
        messages=messages,
    )

    # Extract the content of the response
    answer = response["choices"][0]["message"]["content"].strip()
    return answer


def start_conversation():
    """
    Facilitates a conversation between the user and two agents with distinct personalities.
    The conversation ends when the user types 'exit'.
    """
    agent_1_responses = []  # Track responses from Agent 1
    agent_2_responses = []  # Track responses from Agent 2
    #So they can interact based on the other one awnser.

    while True:
        # Get user input
        user_query = input("Ask a question: ")

        # Check for exit condition
        if user_query.lower() == "exit":
            print("Ending conversation...")
            break

        # Get and display Agent 1's response
        print("\nAgent 1 (Mom):")
        agent_1_response = get_agent_response(
            agent_1_personality, user_query, agent_1_responses
        )
        print(agent_1_response)
        agent_1_responses.append({"role": "assistant", "content": agent_1_response})

        # Get and display Agent 2's response
        print("\nAgent 2 (Kid):")
        agent_2_response = get_agent_response(
            agent_2_personality, user_query, agent_2_responses
        )
        print(agent_2_response)
        agent_2_responses.append({"role": "assistant", "content": agent_2_response})


# Start the chatbot conversation loop
if __name__ == "_main_":
    start_conversation()
