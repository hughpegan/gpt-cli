import sys
import time

from openai import OpenAI

ASSISTANT_ID = 'asst_np9DTw8mwq6VlH5HMM8nBVQy'
THREAD_ID = 'thread_eW1RWL9ZmaXsMGglec38yme7'
COLOR_GREEN = '\033[92m'
COLOR_BLUE = '\033[94m'
COLOR_YELLOW = '\033[96m'
COLOR_RESET = '\033[0m'


def create_new_thread():
    # function that creates a new thread, maybe daily to keep things clean
    return None


def new_user():
    # function that creates assistant, saves assistant id, creates a new thread, saves thread_id, and simple advice on start up
    # like: put money into your playground account, links to guides, how to setup api key
    return None

def get_color():
    terminal_text_color = colorama.get_text_color()
    print(terminal_text_color)


def pretty_print(messages):
    for m in messages:
        return m.content[0].text.value

def generate_response(content):
    client = OpenAI()

    message = client.beta.threads.messages.create(
        thread_id=THREAD_ID, role="user", content=content
    )

    run = client.beta.threads.runs.create(
        thread_id=THREAD_ID,
        assistant_id=ASSISTANT_ID,
    )

    def wait_on_run(run):
        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=THREAD_ID,
                run_id=run.id,
            )
            time.sleep(0.2)
        return run

    run = wait_on_run(run)

    messages = client.beta.threads.messages.list(
        thread_id=THREAD_ID, order="asc", after=message.id
    )

    result = []

    try:
        for m in messages:
            result.append(m.content[0].text.value)
    except Exception as e:
        return f"Error: {str(e)}"

    return result


def main():
    content = " ".join(sys.argv[1:])

    response = generate_response(content=content)

    for r in response:
        print(COLOR_YELLOW + r + COLOR_RESET)


if __name__ == "__main__":
    main()
