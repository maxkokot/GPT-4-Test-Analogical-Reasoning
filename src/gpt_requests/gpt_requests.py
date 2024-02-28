import openai


def ask_gpt4(instruction, options):

    response = None
    message = [{"role": "system", "content": instruction},
               {"role": "user", "content": options}]

    # Make API calls for each line
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message
    )
    # Extracting the assistant's response
    assistant_message = chat_completion['choices'][0]['message']
    if assistant_message['role'] == 'assistant':
        response = assistant_message['content']

    return response
