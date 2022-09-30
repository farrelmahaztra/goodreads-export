# Better Goodreads Export

A small Python script to convert your Goodreads export CSV to JSON and find cover images and links from [Open Library](https://openlibrary.org/). I used this to populate the [books page](https://farrelmahaztra.com/books) on my personal website.

### Installation

```bash
git clone https://github.com/farrelmahaztra/goodreads-export.git
```

### Usage

Move your Goodreads export CSV into the goodreads-export directory (it expects the filename `export.csv` but you can change this variable in the script) and run:

```bash
python3 main.py
```