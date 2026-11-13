from dataclasses import dataclass
from drafter import *
from bakery import assert_equal
import random

@dataclass
class ArtPrompt:
    subject: str
    setting: str
    adjective: str
    full_prompt: str
    favorite: bool
    
@dataclass
class State:
    prompt: list[ArtPrompt]
    current_prompt: str
    custom_subject: str
    selected_setting: str
    generation_count: int

subjects = ["Unicorn", "Duck", "Cake", "Turtle", "Limb", "Horse", "Narwhal", "Cheeseburger", "Car", "Pigeon"]
settings = ["In the Forest", "On a Train", "In a Cave", "On a Skyscraper", "In a Circus Tent", "In a Tomb", "On a Volcano", "In a Prison", "In a Vending Machine", "On TV"]
adjectives= ["Furious", "Curious", "Running", "Melted", "Giant", "Spiky", "Flying", "Rainbow", "Crusty", "Burnt"]

@route
def index(state: State) -> Page:
    """The home page for the website including all the buttons that lead to the other pages.
    Args:
        state(State): dataclass for the website
    Returns:
        Page: The page where the user actual can read or use the website.
    """
    return Page(state, [
        Header("Welcome to Goof Art!"),
        Text("Find a silly prompt for your next project!"),
        "\n",
        Button("Generate a Prompt", "generate_prompt"),
        Button("Random Prompt", "random_prompt"),
        Button("Saved Prompts", "saved_prompts"),
        Button("Favorites", "favorite_prompts"),
        Button("Art Challenges", "art_challenges"),
        Button("About", "about")
    ])

@route
def generate_prompt(state: State) -> Page:
    """The Page where the user can input a subject and click generate.
    Args:
        state(State): dataclass for the website
    Returns:
        Page: The page where the user can genrate an art prompt.
    """
    return Page(state, [
        Header("Custom Prompt Generator"),
        
        Text("Enter a Subject"),
        TextBox("subject"),
        
        Text("Pick a Setting"),
        SelectBox("setting", ["In the forest",
                              "On a train",
                              "In a cave",
                              "On a skyscraper",
                              "In a circus tent",
                              "In a tomb",
                              "On a volcano",
                              "In a prison",
                              "In a vending machine",
                              "On TV"
                            ]),
            
        Button("Generate!", "generate"),
        
        Text(state.current_prompt),
        "\n",
        Button("Home", "index")
        
    ])

@route
def generate(state: State, subject: str, setting:str):
    """Takes the user's input and the selected setting they chose and makes it into a sentence that is the prompt.
    Args:
        state(State): dataclass for the website
        subject(str): the subject of the sentence
        setting(str): the setting in the prompt
    Returns:
        Page: Shows the full sentence and gives options of what to do next.
    """
    state.custom_subject= subject
    state.selected_setting= setting
    
    state.current_prompt= (
        "A " + subject + " " + setting + "!"
    )
    
    state.generation_count += 1
    
    return Page(state, [
        Header("Your Art Prompt!"),
        Text(state.current_prompt),
        Button("Generate Another", "generate_prompt"),
        Button("Home", "index"),
        Button("Save Prompt", "save_prompt")
    ])

@route
def random_prompt(state: State)-> Page:
    """The Page where the user can fully generate a whole random prompt with a button.
    Args:
        state(State): dataclass for the website
    Returns:
        Page: The page where the user can generate the art prompt
    """
    return Page(state, [
        Header("Random Art Prompt"),
        
        Button("Generate!", "randoms"),
        
        Text(state.current_prompt),
        "\n",
        Button("Home", "index")
    ])


@route
def randoms(state: State):
    """Chooses a subject, setting, and adjective randomly and creates a sentence.
    Args:
        state(State): dataclass for the website
    Returns:
        Page: Shows the full random art prompt to the user and gives options of what to do next.
    """
    subjects = ["Unicorn", "Duck", "Cake", "Turtle", "Limb", "Horse", "Narwhal", "Cheeseburger", "Car", "Pigeon"]
    settings = ["In the Forest", "On a Train", "In a Cave", "On a Skyscraper", "In a Circus Tent", "In a Tomb", "On a Volcano", "In a Prison", "In a Vending Machine", "On TV"]
    adjectives= ["Furious", "Curious", "Running", "Melted", "Giant", "Spiky", "Flying", "Rainbow", "Crusty", "Burnt"]

    subject = random.choice(subjects)
    setting = random.choice(settings)
    adjective = random.choice(adjectives)
    
    state.current_prompt = (
        "A " + adjective + " " + subject + " " + setting + "!" 
    )

    state.generation_count += 1

    return Page(state, [
        Text(state.current_prompt),
        Button("Try Again", "random_prompt"),
        Button("Save Prompt", "save_prompt"),
        "\n",
        Button("Home", "index"),
    ])

@route
def saved_prompts(state: State):
    """The page where all the saved prompts go.
    Args:
        state(State): dataclass for the website
    Returns:
        Page: Shows the saved prompts to the user and allows them to save or delete them
    """
    page_components = [
        Header("Saved Prompts")
    ]

    for i in range(len(state.prompt)):

        prompt = state.prompt[i]

        page_components.append(
            Text(prompt.full_prompt)
        )

        if prompt.favorite:
            button_text = "Remove Favorite"
        else:
            button_text = "Add to Favorites"

        page_components.append(
            Button(
                button_text,
                "toggle_favorite",
                [Argument("prompt_index", i)]
            )
        )
    page_components.append(
     Button("Home", "index")
)        
    return Page(state, page_components)
    
@route
def save_prompt(state: State) -> Page:
    """Takes the prompt and adds it to the saved page
    Args:
        state(State): dataclass for the website
    Returns:
        Page: Shows the saved prompt
    """
    new_prompt = ArtPrompt(
        subject=state.custom_subject,
        setting=state.selected_setting,
        adjective="Creative",
        full_prompt=state.current_prompt,
        favorite=False
    )

    state.prompt.append(new_prompt)
    
    return saved_prompts(state)

@route
def favorite_prompts(state: State):
    """Shows the favorites page and the favorited prompts where they can be deleted too.
    Args:
        state(State): dataclass for the website
    Returns:
        Page: The page where the user can view or delete the favorited prompts
    """
    page_components = [
        Header("My Favorite Prompts")
    ]

    for i in range(len(state.prompt)):

        prompt = state.prompt[i]

        if prompt.favorite:

            page_components.append(
                Text(prompt.full_prompt)
            )

            page_components.append(
                Button(
                    "Remove Favorite",
                    "toggle_favorite",
                    [Argument("prompt_index", i)]
                )
            )
    page_components.append(
     Button("Home", "index")
)

    return Page(state, page_components)
    
    
@route
def toggle_favorite(state: State, prompt_index: int):
    """Allows a saved prompt to be favorited.
    Args:
        state(State): dataclass for the website
        prompt_index(int): The index number related to where the words are in the list
    Returns:
        favorite_prompt: Returns the user to the favorite prompt page
    """

    prompt = state.prompt[prompt_index]

    prompt.favorite = not prompt.favorite

    return favorite_prompts(state)

@route
def delete_prompt(state: State, prompt_index: int):
    """Allows a prompt to be deleted
    Args:
        state(State): dataclass for the website
        prompt_index(int): The index number related to where the words are in the list
    Returns:
        favorite_prompt: Returns the user to the favorite prompt page
    """

    state.prompt.pop(prompt_index)

    return favorite_prompts(state)


@route
def art_challenges(state: State) -> Page:
    """Gives five art challenge ideas for the user to read.
    Args:
        state(State): dataclass for the website
    Returns:
        Page: Shows the art challenges to the user
    """
    return Page(state, [
        Header("Art Challenges"),
        
        Text("Choose a Drawing Challenge!"),
        "\n",
        Text("Challenge 1: Find a whiteborad and draw a character that takes up the whole board."),
        "\n",
        Text("Challenge 2: Have your friends give you random words and create characters that represent those words."),
        "\n",
        Text("Challenge 3: Draw using a medium you hate."),
        "\n",
        Text("Challenge 4: Draw a face but roll a die for each facial feature to know how many to draw."),
        "\n",
        Text("Challenge 5: Have a photoshoot with your friends and draw caricatures of the photos."),
        "\n",
        Button("Home", "index")
    ])

@route
def about(state: State) -> Page:
    """Shows what the website is about.
    Args:
        state(State): dataclass for the website
    Returns:
        Page: Shows the writing about the website to the user
    """
    return Page(state, [
        Header("About Goof Art"),
        
        Text("Goof Art is an art prompt generator created as a project for CISC 106."),
        "\n",
        Text("It gives fun inspirations to artists that need some unserious prompts to help with art block or creativity"),
        "\n",
        "\n",
        Text("Goof Art Includes:"),
        "\n",
        Text("Custom Prompt Generator"),
        "\n",
        Text("Random Art Generator"),
        "\n",
        Text("Saved prompts"),
        "\n",
        Text("Art Challenges"),
        "\n",
        Button("Home", "index")
    ])
    
assert_equal(index(State([], "", "", "", 0)).state.prompt, [])
assert_equal(generate_prompt(State([], "", "", "", 0)).state.current_prompt, "")
assert_equal(generate(State([], "", "", "", 0), "Dragon", "In a Cave").state.current_prompt, "A Dragon In a Cave!")
assert_equal(random_prompt(State([], "", "", "", 0)).state.current_prompt, "")
assert_equal(randoms(State([], "", "", "", 0)).state.generation_count, 1)
assert_equal(saved_prompts(State([], "", "", "", 0)).state.prompt, [])
assert_equal(save_prompt(State([], "A Duck In a Cave!", "Duck", "In a Cave", 0)).state.prompt[0].favorite, False)
assert_equal(favorite_prompts(State([], "", "", "", 0)).state.prompt, [])
assert_equal(toggle_favorite(State([ArtPrompt("Duck", "In a Cave", "Creative", "A Duck In a Cave!", False)], "", "", "", 0), 0).state.prompt[0].favorite, True)
assert_equal(delete_prompt(State([ArtPrompt("Duck", "In a Cave", "Creative", "A Duck In a Cave!", False)], "", "", "", 0), 0).state.prompt, [])
assert_equal(art_challenges(State([], "", "", "", 0)).state.prompt, [])
assert_equal(about(State([], "", "", "", 0)).state.prompt, [])

initial_state = State(
    prompt=[],
    current_prompt="",
    custom_subject="",
    selected_setting="",
    generation_count=0
)

start_server(initial_state)
