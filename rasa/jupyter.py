import pprint as pretty_print
from typing import Any, Dict, Text, TYPE_CHECKING
from rasa_core.utils import print_success, print_error
from rasa_core.interpreter import NaturalLanguageInterpreter, RasaNLUInterpreter
import rasa.model as model

if TYPE_CHECKING:
    from rasa_core.agent import Agent


def pprint(object: Any):
    pretty_print.pprint(object, indent=2)


def chat(model_path: Text = None, agent: 'Agent' = None,
         interpreter: NaturalLanguageInterpreter = None) -> None:
    """Chat to the bot within a Jupyter notebook.

    Args:
        model_path: Path to a Rasa Stack model.
        agent: Rasa Core agent (used if no Rasa Stack model given).
        interpreter: Rasa NLU interpreter (used with Rasa Core agent if no
                     Rasa Stack model is given).
    """

    if model_path:
        from rasa.run import create_agent
        unpacked = model.get_model(model_path)
        agent = create_agent(unpacked)
    elif agent and interpreter:
        # HACK: this skips loading the interpreter and directly 
        # sets it afterwards
        nlu_interpreter = RasaNLUInterpreter("skip this and use given "
                                             "interpreter", lazy_init=True)
        nlu_interpreter.interpreter = interpreter
        agent.interpreter = interpreter
    else:
        print_error("You either have to define a model path or an agent and "
                    "an interpreter.")

    print("Your bot is ready to talk! Type your messages here or send '/stop'.")
    while True:
        message = input()
        if message == '/stop':
            break

        for response in agent.handle_text(message):
            _display_bot_response(response)


def _display_bot_response(response: Dict):
    from IPython.display import Image, display

    for response_type, value in response.items():
        if response_type == 'text':
            print_success(value)

        if response_type == 'image':
            image = Image(url=value)
            display(image,)
