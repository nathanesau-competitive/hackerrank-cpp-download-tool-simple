# hackerrank-cpp-download-tool-simple

## Dependencies

1. Install ``vscode``
2. Install ``vscode-cpptools`` extension
3. Install ``vscode-cmake-tools`` extension

## Usage

First clone this repository using ``git clone https://github.com/nathanesau-competitive/hackerrank-cpp-download-tool-simple``.

Then, it is time to use the Python scripts.

### Download script:

Some examples are shown below:

    python download.py ctci-ransom-note
    python download.py special-palindrome-again
    python download.py count-triplets-1

### Using downloaded files

After running the download script, code your solution in ``main.cpp``. Then compile (F7) and debug (F5).

Output gets written to ``output.txt`` (some tweaks to ``main.cpp`` may be needed for this part)

* To change the test case, change variables ``inputFName`` and ``outputFName``
* ``output.txt`` is compared to test cases, for instance ``output/output00.txt``
* An assert is triggered if the output is different than expected.

### Clean script:

The clean script is used to delete the downloaded files from the current directory. Clean should be done before downloading a new challenge.

    python clean.py