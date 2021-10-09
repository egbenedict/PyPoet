# PyPoet

A program to auto-generate 3-line poems. Originally intended to produce haikus, the syllabic condition has since been removed in order to provide greater 
flexibility of expression. The main goal of this project was to produce computer-generated poems that contained some sense of tangible meaning. Though several
other such projects around the web utilize neural networks (to varying degrees of success), I opted against that approach. Instead, this program extracts a random
grammatical structure from one of tens of thousands of poems in `poems.txt` (source: Herval Freire’s [Haikuzao](https://github.com/herval/creative_machines/blob/master/haikuzao/src/main/resources/haiku.txt) corpus).
Then it randomly selects a primary, or pivot, noun to serve as the subject of the poem (one can also provide this noun directly beforehand to generate specific poems).
The program then iteratively fills up the predetermined grammatical structure, utilizing the [Datamuse API](https://www.datamuse.com/api/) to help string words and
phrases together with meaning.

Admittedly, this project has been a lot harder than I thought it would be, and as of right now most of the poems outputted are gibberish. I'd say approximately 1 out of every 15-20 poems
can be accepted as at least 'decent'. There are also still a few bugs that I have yet to fix in future commits. Hopefully I'll find time to continue working on this project
at some point and further increase the quality of poems produced (my next version might try incorporating a neural network).

## Dependencies
- [NLTK](https://www.nltk.org/install.html)

## Use
- If desired, provide a subject noun on line 85 in `haiku.py`
- For a random poem, comment out line 85 
- Run `python3 haiku.py` from the command line
