import json
import re
from datetime import datetime
from pathlib import Path

import inflect as ifl
import pyperclip
from InquirerPy.base import Choice
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError

import prompts

inflect = ifl.engine()

this_dir = Path(__file__).parent
licenses_dir = this_dir / "licenses"


def save_license(gitignore: str, use_cwd: bool = False) -> None:
    while True:
        if use_cwd:
            save_path = Path.cwd() / "LICENSE.md"
        else:
            def path_postprocessor(path: str) -> str:
                path = Path(path) / "LICENSE.md"

                path.parent.mkdir(parents=True, exist_ok=True)
                return path.expanduser().resolve()

            save_path = prompts.filepath(
                message="Where should your license be saved?",
                instruction="Enter a path.",
                long_instruction="Both absolute and relative paths are supported.\n"
                                 "Nonexistent directories will be created as necessary.",
                multicolumn_complete=True,
                only_directories=True,
                validate=lambda path: bool(path),
                invalid_message="You must enter a path.",
                filter=path_postprocessor,
                transformer=path_postprocessor).execute()

        if save_path.exists():
            overwrite_choices = [
                Choice(name="Overwrite it", value=True),
                Choice(name="Choose another place", value=False),
            ]

            overwrite = prompts.select(
                message="A LICENSE.md file already exists there. What do you wanna do?",
                choices=overwrite_choices).execute()

            if overwrite:
                save_path.write_text(gitignore)
                break
            else:
                use_cwd = False
                continue

        else:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(gitignore)
            break

    print(f"\nLICENSE.md saved to {save_path}.")


def get_oss_license() -> Path:
    oss_dir = licenses_dir / "markdown-licenses"

    metadata = json.load((licenses_dir / "oss_metadata.json").open())
    license_choices = [Choice(name=name, value=oss_dir / path) for
                       path, name in metadata.items()]

    license_choices.sort(key=lambda choice: choice.name)

    selected_license = prompts.fuzzy(
        message="Choose a license.",
        instruction="You can type to search for a specific one.",
        choices=license_choices,
    ).execute()

    if selected_license.stem in ["mit", "bsd-2", "bsd-3"]:
        year = prompts.number(
            message="Enter the copyright year.",
            default=datetime.now().year,
            validate=lambda result: int(result) <= datetime.now().year,
            invalid_message=f"The copyright year must be less than or equal to {datetime.now().year}.",
        ).execute()

        authors: list = prompts.text(
            message="Enter a comma-and-space-separated list of copyright holders.",
            validate=lambda result: len(result) > 0,
            invalid_message="You must enter at least one copyright holder.",
            filter=lambda result: inflect.join(result.split(", ")),
        ).execute()

        with selected_license.open() as f:
            license_text = f.read()

            if year:
                license_text = re.sub(r"`<year>`", year, license_text, flags=re.IGNORECASE)

            if authors:
                license_text = re.sub(r"`<owner>`|`<copyright holders?>`", authors, license_text, flags=re.IGNORECASE)
    else:
        license_text = selected_license.read_text()

    return license_text


def get_cc_license() -> str:
    class CCPropertyValidator(Validator):
        def validate(self, document: Document) -> None:
            if "zero" in document.text and len(document.text) > 1:
                raise ValidationError(message="If you choose Zero, it must be the only property you choose.")

            if "nd" in document.text and "sa" in document.text:
                raise ValidationError(message="You can't choose both No Derivatives and Share-Alike.")

    def cc_property_transformer(result: str) -> str:
        props = {
            "Non-Commercial": "NC",
            "No Derivatives": "ND",
            "Share-Alike": "SA",
        }

        return "BY-" + "-".join([props.get(prop, "Creative Commons Zero") for prop in result])

    cc_dir = licenses_dir / "Creative-Commons-Markdown"

    properties = prompts.select("Choose your license's properties.",
                                choices=[Choice(name="Non-Commercial", value="nc"),
                                         Choice(name="No Derivatives", value="nd"),
                                         Choice(name="Share-Alike", value="sa"),
                                         Choice(name="Zero (Public Domain)", value="zero")],
                                validate=CCPropertyValidator(),
                                transformer=cc_property_transformer,
                                multiselect=True).execute()

    if "zero" in properties:
        license_text = (cc_dir / "latest" / "zero.markdown").read_text()
    else:
        versions = sorted([float(path.name) for path in cc_dir.glob("[0-9].[0-9]")])
        version = prompts.select(
            message="Choose your license's version.",
            instruction=f"If you're unsure, choose {max(versions)}.",
            choices=versions,
            default=max(versions),
        ).execute()

        license_text = (cc_dir / str(version) / f"{'by-' + '-'.join(properties)}.markdown").read_text()

    return license_text


def main():
    category = prompts.select(
        message="Choose a category.",
        choices=[Choice(name="Open source licenses", value="oss"), Choice(name="Creative Commons licenses", value="cc")]
    ).execute()

    if category == "oss":
        license_text = get_oss_license()
    else:
        license_text = get_cc_license()

    output = prompts.select(
        message="Choose how to save your license.",
        choices=[Choice(name="Save to current directory", value="cwd"),
                 Choice(name="Save to another directory", value="elsewhere"),
                 Choice(name="Print to stdout", value="stdout"),
                 Choice(name="Copy to clipboard", value="clipboard")]
    ).execute()

    if output == "cwd":
        save_license(license_text, use_cwd=True)
    elif output == "elsewhere":
        save_license(license_text)
    elif output == "stdout":
        print(license_text)
    elif output == "clipboard":
        pyperclip.copy(license_text)


main()
