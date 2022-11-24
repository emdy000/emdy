# Emdy

Emdy generates Markdown-formattted open source and Creative Commons licenses from your command line.

## Installation

### pipx (recommended)

The recommended, cross-platform way of installing Emdy is via [pipx](https://pypa.github.io/pipx/).

```bash
pipx install emdy
```

### Homebrew (macOS and Linux)

A [Homebrew](https://brew.sh) formula for Emdy is available from
the [Houkago Tea Tap](https://github.com/celsiusnarhwal/homebrew-htt).

```bash
brew tap celsiusnarhwal/htt
brew install emdy
```

### pip (not recommended)

Emdy can be installed via pip like any other Python package, but unless you're going to create a virtual environment
for it yourself, you're strongly recommeded to use pipx or Homebrew.

```bash
pip install emdy
```

## Usage

Simply invoke Emdy from the command line:

```bash
emdy
```

That's it. Emdy will interactively guide you through the rest.

See it in action below.

<figure>
    <img src="media/oss_demo.gif" alt="Using Emdy to generate an MIT License.">
    <figcaption>Using Emdy to generate an MIT License.</figcaption>
</figure>

<br>

<figure>
    <img src="media/cc_demo.gif" alt="Using Emdy to generate a CC BY-SA 4.0 License.">
    <figcaption>Using Emdy to generate a CC BY-SA 4.0 License.</figcaption>
</figure>

## Acknowledgements

Emdy sources its Markdown-formatted licenses
from [IQAndreas/markdown-licenses](https://github.com/IQAndreas/markdown-licenses)
and [idleberg/Creative-Commons-Markdown](https://github.com/idleberg/Creative-Commons-Markdown).

## Disclaimer

Licenses produced by Emdy have been modified from their original forms. I'm not responsible for any legal issues
arising from inconsistencies between Emdy's licenses and those they were derived from.

## License

Emdy is licensed under the [MIT License](https://github.com/celsiusnarhwal/emdy/blob/HEAD/LICENSE.md).